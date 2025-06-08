#!/bin/bash

client_mac=$1
username=$2
password=$3

auth_url=$(cat auth_url.conf)
auth_protocol=$(cat auth_protocol.conf)

echo auth_url

case $auth_protocol in

  LDAP)
    LDAP_query=$(cat LDAP_query.conf)
    ldapsearch -x -H $auth_url -D "uid=$username,$LDAP_query" -b "$LDAP_query" -s sub "(uid=$username)" -w $password
    exit $?
    ;;

  HTTP)
    curl -u $username:$password $auth_url
    exit $?
    ;;

  RADIUS)
    radius_secret=$(cat radius_secret.conf)
    radius_port=$(cat radius_port.conf)
#     python -c "import radius; exit(0 if radius.authenticate('$username', '$password', '$radius_secret', host='$auth_url', port=$radius_port) else 1)"
    echo "User-Name = $username,User-Password = $password" | radclient -x -s $auth_url auth $radius_secret
    exit $?
    ;;

  *)
    exit 1
    ;;
esac

exit 0
