import os
import requests
import json
import logging
from typing import Optional, Dict, List, Union

# Configuration
TIMEOUT = 10
NEXT_DNS_API = "https://api.nextdns.io"
API_PROFILE_ROUTE = "profiles"

API_KEY = os.getenv("NEXTDNS_API_KEY")

PROFILE_MAIN = os.getenv("NEXTDNS_PROFILE_MAIN")
PROFILE_RPM = os.getenv("NEXTDNS_PROFILE_RPM")
PROFILE_BETSY = os.getenv("NEXTDNS_PROFILE_BETSY")
PROFILE_LEONA = os.getenv("NEXTDNS_PROFILE_LEONA")
PROFILE_HURLEY = os.getenv("NEXTDNS_PROFILE_HURLEY")
PROFILE_SYNC_LIST = [PROFILE_RPM, PROFILE_BETSY, PROFILE_LEONA, PROFILE_HURLEY]

TLD_BAN_LIST = sorted(set([
    "autos", "best", "bid", "bio", "boats", "boston", "boutique", "charity",
    "christmas", "dance", "fishing", "hair", "haus", "loan", "loans", "men",
    "mom", "name", "review", "rip", "skin", "support", "tattoo", "tokyo",
    "voto", "sbs", "ooo", "gdn", "zip"
]))
TLD_BAN_LIST_DICT = [{'id': tld} for tld in TLD_BAN_LIST]
TLD_BAN_PAYLOAD = {"tlds": TLD_BAN_LIST_DICT}

HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def setup_logger(name: str) -> logging.Logger:
    """Sets up a logger with a given name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all messages
    
    # Create a stream handler and set its format
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s')
    handler.setFormatter(formatter)
    
    # Add the handler if it doesn't already exist
    if not logger.hasHandlers():
        logger.addHandler(handler)
    
    return logger

logger = setup_logger(__name__)

def api_request(method: str, url: str, headers: Optional[Dict[str, str]] = None,
                data: Optional[Union[Dict, str]] = None, json: Optional[Dict] = None,
                timeout: int = TIMEOUT) -> requests.Response:
    """
    Makes an HTTP request and handles errors.

    Args:
        method (str): HTTP method (GET, POST, PATCH, etc.).
        url (str): The endpoint URL.
        headers (dict, optional): Headers to include in the request.
        data (dict, optional): Data to send in the body of the request (for POST, PATCH).
        json (dict, optional): JSON data to send in the body of the request (for POST, PATCH).
        timeout (int): Timeout for the request.

    Returns:
        Response: The HTTP response object.

    Raises:
        Exception: If the request returns a 400 Bad Request, or any other HTTP error.
    """
    logger.info("[API CALL] USING %s", method)
    if data is not None:
        logger.info("[API CALL] Using payload %s", json.dumps(data, separators=(',', ':')))
    
    try:
        response = requests.request(method, url, headers=headers, data=data, json=json, timeout=timeout)
        response.raise_for_status()
        if response.status_code not in (200, 204):
            logger.info("[API CALL] Response: %s", response.text)
        else:
            logger.info("[API CALL] Request succeeded")
        return response
    except requests.exceptions.RequestException as e:
        logger.error("[API CALL] Request failed: %s", e)
        raise

def fetch_profile_settings(profile_id: str) -> Dict:
    """Fetches the settings for a given profile ID."""
    url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/"
    response = api_request("GET", url, headers=HEADERS)
    return response.json()

def filter_blocklists(blocklists: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filter blocklists to only include the 'id' field."""
    return [{"id": blocklist.get("id")} for blocklist in blocklists if blocklist.get("id")]

def build_payload(data: Dict, keys_to_sync: List[str]) -> Dict:
    """Build payload for syncing settings."""
    return {key: data.get(key, []) for key in keys_to_sync if data.get(key) is not None}

def alpha_sort_lists(data: Dict) -> Dict:
    """Sorts the allowlist and denylist alphabetically by 'id'."""
    if "allowlist" in data:
        data["allowlist"] = sorted(data["allowlist"], key=lambda x: x['id'])
    if "denylist" in data:
        data["denylist"] = sorted(data["denylist"], key=lambda x: x['id'])
    return data

def update_profile_settings(profile_id: str, payload: Dict, route: Optional[str] = None, method: str = "PATCH") -> requests.Response:
    """Updates the settings for a given profile ID."""
    logger.info("[UPDATE-PROFILE] Updating profile settings for profile %s...", profile_id)
    url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/{route if route else 'settings'}"
    if payload is None:
        raise ValueError("[UPDATE-PROFILE] Payload cannot be None. Please provide a valid payload.")
    return api_request(method, url, headers=HEADERS, json=payload)

def update_array_settings(profile_id: str, key: str, payload: List[Dict], route: Optional[str] = None, method: str = "PUT") -> requests.Response:
    """Updates array settings like denylist or blocklists."""
    logger.info("[UPDATE-ARRAY] Updating array settings for profile %s...", profile_id)
    url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/{route if route else key}"
    if not isinstance(payload, list):
        raise ValueError("[UPDATE-ARRAY] Payload must be a list for array updates.")
    logger.info("[UPDATE-ARRAY] Url for [%s] is %s", profile_id, url)
    return api_request(method, url, headers=HEADERS, json=payload)

def update_security_settings(profile_id: str, tlds_payload: Dict, method: str = "PATCH") -> requests.Response:
    """Updates security settings for the profile."""
    url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/security"
    logger.info("[UPDATE-SECURITY] Updating security settings for profile %s...", profile_id)
    try:
        response = api_request(method, url, headers=HEADERS, json=tlds_payload)
        logger.info("[UPDATE-SECURITY] Request succeeded")
        return response
    except Exception as e:
        logger.error("[UPDATE-SECURITY] Failed to update security settings: %s", e)
        raise

def sync_profiles(keys_to_sync: List[str], payload: Optional[Dict] = None) -> None:
    """Syncs settings from the main profile to the target profiles."""
    try:
        settings = fetch_profile_settings(PROFILE_MAIN)
        data = settings['data']
        logger.info("[SYNC] Settings from Profile %s", PROFILE_MAIN)
        
        if payload is None:
            payload = build_payload(data, keys_to_sync)
        
        payload = alpha_sort_lists(payload)
        logger.info("[SYNC] Generated Payload: %s", json.dumps(payload, separators=(',', ':')))

        for profile_id in PROFILE_SYNC_LIST:
            for key in keys_to_sync:
                if key in payload:
                    key_payload = payload[key]
                    logger.info("[SYNC] Using Key [%s]", key)
                    if "blocklists" in key_payload:
                        logger.info("[SYNC] [blocklists] to be filtered")
                        key_payload["blocklists"] = filter_blocklists(key_payload["blocklists"])
                    try:
                        if isinstance(key_payload, list):
                            update_array_settings(profile_id, key, key_payload)
                        else:
                            update_profile_settings(profile_id, key_payload, key)
                        logger.info("[SYNC] Successfully updated %s for profile %s.", key, profile_id)
                    except Exception as e:
                        logger.error("[SYNC] Failed to update %s for profile %s: %s", key, profile_id, e)

    except Exception as e:
        logger.error("[SYNC] Failed to sync profiles: %s", e)
        raise

# Run the sync process
keys_to_sync = ["allowlist", "denylist", "parentalControl", "security", "privacy"]
sync_profiles(keys_to_sync)

# Ad Hoc Main Updates
update_security_settings(PROFILE_MAIN, TLD_BAN_PAYLOAD)
