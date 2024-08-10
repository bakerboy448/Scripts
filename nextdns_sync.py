import requests
import json
import logging


TIMEOUT = 10
NEXT_DNS_API = "https://api.nextdns.io"
API_PROFILE_ROUTE = "profiles"
API_KEY = "REMOVED"

PROFILE_MAIN = "REMOVED"
PROFILE_RPM = "REMOVED"
PROFILE_BETSY = "REMOVED"
PROFILE_LEONA = "REMOVED"
PROFILE_HURLEY = "REMOVED"
profile_sync_list = [PROFILE_RPM, PROFILE_BETSY, PROFILE_LEONA, PROFILE_HURLEY]

TLD_BAN_LIST = [
    "autos", "best", "bid", "bio", "boats", "boston", "boutique", "charity",
    "christmas", "dance", "fishing", "hair", "haus", "loan", "loans", "men",
    "mom", "name", "review", "rip", "skin", "support", "tattoo", "tokyo",
    "voto", "sbs", "ooo", "gdn", "zip"
]
TLD_BAN_LIST = sorted(set(TLD_BAN_LIST))
TLD_BAN_LIST_DICT = [{'id': tld} for tld in TLD_BAN_LIST]
TLD_BAN_PAYLOAD = {"tlds": TLD_BAN_LIST_DICT}

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def setup_logger(name):
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

# Create a logger instance with the current module name
logger = setup_logger(__name__)

def api_request(method, url, headers=None, data=None, json=None, timeout=10):
    """
    Makes an HTTP request and handles 400 Bad Request errors by throwing the full response.
    
    Args:
        method (str): HTTP method (GET, POST, PATCH, etc.).
        url (str): The endpoint URL.
        headers (dict): Optional headers to include in the request.
        data (dict): Data to send in the body of the request (for POST, PATCH).
        json (dict): JSON data to send in the body of the request (for POST, PATCH).
        timeout (int): Timeout for the request.
    
    Returns:
        dict: The JSON response if the request is successful.
    
    Raises:
        Exception: If the request returns a 400 Bad Request, or any other HTTP error.
    """
    logger.info("[API CALL] USING %s", method)
    if data is not None:
        logger.info("[API CALL] Using payload {json.dumps(data, separators=(',', ':'))}")
    response = requests.request(method, url, headers=headers, data=data, json=json, timeout=timeout)
    response_code = response.status_code
    if response_code == 400:
        raise Exception(f"[API CALL] Bad Request: {response.status_code} - {response.text}")
    response.raise_for_status()
    if response_code not in (200, 204):
        logger.info("[API CALL] Response: %s", response)
    else:
        logger.info("[API CALL] Request succeeded")
    return response

# Using make_request in fetch_profile_settings
def fetch_profile_settings(profile_id):
    """Fetches the settings for a given profile ID and returns the allowlist and denylist."""
    url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/"
    return api_request("GET", url, headers=headers, timeout=TIMEOUT)


def filter_blocklists(blocklists):
    """Filter blocklists to only include the 'id' field."""
    return [{"id": blocklist.get("id")} for blocklist in blocklists if blocklist.get("id")]


def build_payload(data, keys_to_sync):
    return {key: data.get(key, []) for key in keys_to_sync if data.get(key) is not None}


def alpha_sort_lists(data):
    """Sorts the allowlist and denylist alphabetically by 'id'."""
    if "allowlist" in data:
        data["allowlist"] = sorted(data["allowlist"], key=lambda x: x['id'])
    if "denylist" in data:
        data["denylist"] = sorted(data["denylist"], key=lambda x: x['id'])
    return data


# Using make_request in update_profile_settings
def update_profile_settings(profile_id, payload, route=None, method="PATCH"):
    """Updates the settings for a given profile ID using the provided allowlist and denylist."""
    logger.info(f"[UPDATE-PROFILE] Updating profile settings for profile {profile_id}...")
    if route is None:
        url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/settings"
    else:
        url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/{route}"
        
    if payload is None:
        raise ValueError("[UPDATE-PROFILE] Payload cannot be None. Please provide a valid payload.")
    return api_request(method, url, headers=headers, json=payload, timeout=TIMEOUT)


def update_array_settings(profile_id, key, payload, route=None, method="PUT"):
    """Updates array settings like denylist or blocklists."""
    logger.info(f"[UPDATE-ARRAY] Updating array settings for profile {profile_id}...")
    if route is None:
        url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/{key}"
    else:
        url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/{route}/{key}"

    if not isinstance(payload, list):
        raise ValueError("[UPDATE-ARRAY] Payload must be a list for array updates.")
    logger.info("[UPDATE-ARRAY] Url for [%s] is %s", profile_id, url)
    return api_request(method, url, headers=headers, json=payload, timeout=TIMEOUT)


def update_security_settings(profile_id, tlds_payload, method="PATCH"):
    url = f"{NEXT_DNS_API}/{API_PROFILE_ROUTE}/{profile_id}/security"
    
    logger.info(f"[UPDATE-SECURITY] Updating security settings for profile {profile_id}...")
    logger.info(f"[UPDATE-SECURITY] url for [{profile_id}] is {url}")
    try:
        response = api_request(method, url, headers=headers, json=tlds_payload, timeout=TIMEOUT)
        logger.info("[UPDATE-SECURITY] Request succeeded")
        return response
    except Exception as e:
        logger.error(f"[UPDATE-SECURITY] Failed to update security settings: {e}")
        raise


def sync_profiles(keys_to_sync, payload=None):
    """Syncs the allowlist, denylist, and other settings from the main profile to the target profiles."""
    try:
        settings = fetch_profile_settings(PROFILE_MAIN).json()
        data = settings['data']
        logger.info("[SYNC] Settings from Profile [PROFILE_MAIN]: %s", PROFILE_MAIN)
        
        if payload is None:
            payload = build_payload(data, keys_to_sync)
        # Alpha sort allowlist and denylist
        payload = alpha_sort_lists(payload)
        logger.info("[SYNC] Generated Payload:")
        logger.info(f"[SYNC] Using payload {json.dumps(data, separators=(',', ':'))}")

        for profile_id in profile_sync_list:
            for key in keys_to_sync:
                if key in payload:
                    key_payload = payload[key]
                    logger.info("[SYNC] Using Key [%s]", key)
                    logger.debug(f"[SYNC] Payload is {key_payload}")
                    if "blocklists" in key_payload:
                        logger.info("[SYNC] [blocklists] to be filtered")
                        logger.debug("[SYNC] Pre Filter of [privacy][blocklists]")
                        key_payload["blocklists"] = filter_blocklists(key_payload["blocklists"])
                        logger.debug("[SYNC]  Filtered [blocklists]")
                        logger.debug(key_payload["blocklists"])
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
## TLDs
# update_security_settings(PROFILE_MAIN, TLD_BAN_PAYLOAD)
