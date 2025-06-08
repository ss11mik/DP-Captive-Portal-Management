"""
Filename: __init__.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import imgkit

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

from CPM.modules.utils import Utils


def remove_settings_portal(self, portal_id):
    self.config.remove_section("portal." + portal_id)
    self.reload_from_config()


def apply_settings_portal(self, portal_id, params):
    for key in params.keys():
        for value in params.getlist(key):
            self.config.set_for_portal(portal_id, key, value)
    # self.portals[portal_id].apply_auth()
    self.reload_from_config()


def apply_auth_to_portal(self, portal_id, auth_server_name):
    auth_protocol = self.config.get_from_auth_server(auth_server_name, 'auth_protocol')
    auth_url = self.config.get_from_auth_server(auth_server_name, 'auth_url')
    auth_timeout = self.config.get_from_auth_server(auth_server_name, 'auth_timeout')
    auth_method = self.config.get_from_auth_server(auth_server_name, 'auth_method')
    radius_secret = self.config.get_from_auth_server(auth_server_name, 'radius_secret')
    ldap_query = self.config.get_from_auth_server(auth_server_name, 'ldap_query')
    self.portals[portal_id].apply_auth(auth_protocol, auth_url, auth_timeout, auth_method, radius_secret, ldap_query)


def get_portals(self):
    portal_ids = self.config.get_portals()
    portals = []
    selected_portals = self.config.get_selected_portals()

    for portal_id in portal_ids:
        portals += [{
            "id": portal_id,
            "implementation": self.config.get_from_portal(portal_id, "implementation"),
            "connection": self.config.get_from_portal(portal_id, "connection"),
            "auth_server": self.config.get_from_portal(portal_id, "auth_server"),
            "current_single": self.config.get_single_portal() == portal_id,
            "selected": portal_id in selected_portals,
            "theme": self.get_applied_theme_id(portal_id)
        }]

    return portals


def get_portals_for_status(self):
    portal_ids = self.config.get_portals()
    portals = []
    selected_portals = self.config.get_selected_portals()

    for portal_id in portal_ids:
        if portal_id in selected_portals:
            portals += [{
                "id": portal_id,
                "implementation": self.config.get_from_portal(portal_id, "implementation"),
                "connection": self.config.get_from_portal(portal_id, "connection"),
                "status": self.get_status(portal_id),
                "is_running": self.is_running(portal_id)
            }]

    return portals


def create_portal(self, portal_id, implementation, connection, auth_server):
    self.config.create_portal(portal_id, implementation, connection, auth_server)
    self.reload_from_config()


def get_single_portal(self):
    return self.config.get_single_portal()

def get_single_auth_server(self):
    return self.config.get_from_single_portal("auth_server")

def get_available_captive_portal_implementations(self):
    return self.app.config["PORTAL_IMPLEMENTATIONS"]

