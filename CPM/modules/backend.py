"""
Filename: backend.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import traceback

from CPM.modules.portals import NDS, pfSense
from CPM.modules.connection import Connection, Local, Remote_SSH
from CPM.modules.auth_servers import Abstract_Auth_Server, HTTP_Auth_Server, Simple_Auth_Server, FreeRADIUS_Auth_Server, LLDAP_Auth_Server


def init_backends(app, config):
    portals = {}
    auth_servers = {}

    portal_names = config.get_portals()
    auth_server_names = config.get_auth_servers()

    for portal_name in portal_names:
        try:
            connection_name = config.get_from_portal(
                portal_name, "connection")
            connection = init_connection(config, connection_name)

            portals[portal_name] = init_portal(
                config, portal_name, connection)
        except Exception:
            traceback.print_exc()


    for auth_server_name in auth_server_names:
        try:
            connection_name = config.get_from_auth_server(
                auth_server_name, "connection")
            connection = init_connection(config, connection_name)

            auth_servers[auth_server_name]= init_auth_server(app, config, auth_server_name, connection)
        except Exception:
            traceback.print_exc()

    print(portals)
    return portals, auth_servers


def init_connection(config, connection_name):
    connection_type = config.get_from_connection(connection_name, "connection_type")
    if connection_type == "local":
        connection = Local(None)
    elif connection_type == "SSH":
        connection = Remote_SSH(config.get_section(
            "connection." + connection_name))
    else:
        raise Exception("Unknown connection type:" + connection_type)

    return connection


def init_portal(config, portal_name, connection):
    portal_implementation = config.get_from_portal(portal_name, "implementation")
    if portal_implementation == "NDS":
        portal = NDS(config.get_section(
            "portal." + portal_name), connection)
    # if app.config['PORTAL_PROVIDER'] == "OpenNDS":
    # if app.config['PORTAL_PROVIDER'] == "Coova":
    elif portal_implementation == "pfSense":
        portal = pfSense(config.get_section(
            "portal." + portal_name), connection)
    else:
        raise Exception("Unknown portal implementation: " + portal_name)

    return portal

def init_auth_server(app, config, auth_server_name, connection):
    protocol = config.get_from_auth_server(auth_server_name, "protocol")
    url = config.get_from_auth_server(auth_server_name, "url")
    userfile = config.get_from_auth_server(auth_server_name, "userfile")

    connection_name = config.get_from_auth_server(
        auth_server_name, "connection")
    connection = init_connection(config, connection_name)

    if protocol == "simple":
        auth_server = Simple_Auth_Server(url, connection, userfile)
    elif protocol == "HTTP":
        auth_server = HTTP_Auth_Server(url, connection, userfile)
    elif protocol == "LLDAP":
        auth_server = LLDAP_Auth_Server(url, connection, userfile, app.config['THEMES_FOLDER'])
    elif protocol == "FreeRADIUS":
        auth_server = FreeRADIUS_Auth_Server(url, connection, userfile)
    else:
        raise Exception("Unknown authentication server protocol: " + protocol)

    return auth_server
