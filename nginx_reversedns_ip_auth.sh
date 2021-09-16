#!/bin/bash
${HOSTNAME:=domain.com}
${nginxpath:='/etc/nginx/snippets/'}
${types:='ip-auth.conf'}

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

if [[ $(pgrep -acx apache | wc -l) -gt "0" ]]; then
    echo "Apache detected; This script only supports NGINX."
    exit 2
fi
if [[ $(pgrep -acx nginx | wc -l) -gt "0" ]]; then
    echo "NGINX detected"
else
    echo "NGINX not not detected; NGINX is required"
    exit 3
fi
if [[ $(sudo ufw status | grep -qw active) -gt "0" ]]; then
    echo "UFW detected"
else
    echo "UFW not not detected; UFW is required"
    exit 4
fi

regex_ip="(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
echo host is [$HOSTNAME]
new_ip=$(host $HOSTNAME | grep -E -o "$regex_ip")
old_ip=$(/usr/sbin/ufw status | grep $HOSTNAME | grep -E -o "$regex_ip" | head -n1)

if [ "$new_ip" = "$old_ip" ]; then
    echo IP address has not changed - old: [$old_ip] new:[$new_ip]
else
    echo IP address has changed - old: [$old_ip] new:[$new_ip]
    echo trying to delete old ufw rules
    if [ -n "$old_ip" ]; then
        # ToDo Create loops.  Verify and create rules if needed
        /usr/sbin/ufw delete allow from "$old_ip" to any app radarr comment "$HOSTNAME"
        /usr/sbin/ufw delete allow from "$old_ip" to any app radarr4k comment "$HOSTNAME"
        /usr/sbin/ufw delete allow from "$old_ip" to any app readarr comment "$HOSTNAME"
        /usr/sbin/ufw delete allow from "$old_ip" to any app sonarr comment "$HOSTNAME"
        /usr/sbin/ufw delete allow from "$old_ip" to any app prowlarr comment "$HOSTNAME"
        echo rules deleted
    fi
    # ToDo Create loops.  Verify and create rules if needed
    echo adding new ufw rules
    /usr/sbin/ufw allow from "$new_ip" to any app radarr comment "$HOSTNAME"
    /usr/sbin/ufw allow from "$new_ip" to any app radarr4k comment "$HOSTNAME"
    /usr/sbin/ufw allow from "$new_ip" to any app readarr comment "$HOSTNAME"
    /usr/sbin/ufw allow from "$new_ip" to any app sonarr comment "$HOSTNAME"
    /usr/sbin/ufw allow from "$new_ip" to any app prowlarr comment "$HOSTNAME"
    echo rules added
    echo iptables have been updated
fi

# ToDo Clean up; create and verify a specifc nginx conf file for auth
new_nginx_auth="allow $new_ip; #$HOSTNAME"
echo new nginx auth ["$new_nginx_auth"]
old_nginx_ip=$(grep --include=$types -rnw $nginxpath -e "#$HOSTNAME" | grep -E -o "$regex_ip" | head -n1)
echo old nginx ip detected as ["$old_nginx_ip"]
old_nginx_auth="allow $old_nginx_ip; #$HOSTNAME"
echo old nginx auth ["$old_nginx_auth"]
if [ "$new_ip" = "$old_nginx_ip" ]; then
    echo nginx auth does not need to be changed
else
    echo nginx auth does need to be changed
    echo updating ["$old_nginx_ip"] to ["$new_ip"] in ["$nginxpath""$types"]
    sed -i s/"$old_nginx_ip"/"$new_ip"/g $nginxpath$types
    echo updated ip is ["$(grep --include=$types -rnw $nginxpath -e "#$HOSTNAME" | grep -E -o "$regex_ip" | head -n1)"]
    echo reloading nginx
    nginx -s reload
    echo nginx auth been updated
    exit 0
fi
