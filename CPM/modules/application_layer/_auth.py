"""
Filename: _auth.py
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


def set_auth_for_portal_user_pwd(self, portal_id, params):
    auth_protocol = params.getlist("auth_protocol")[0]
    auth_url = params.getlist("auth_url")

    self.config.set("portal." + portal_id, "auth_protocol", auth_protocol)
    self.config.set("portal." + portal_id, "auth_url", auth_url)

def apply_auth(self, auth_server_id, params):
    protocol = params.getlist("protocol")[0]
    url = params.getlist("url")[0]
    userfile = params.getlist("userfile")[0]

    self.config.set_for_auth_server(auth_server_id, "protocol", protocol)
    self.config.set_for_auth_server(auth_server_id, "url", url)
    self.config.set_for_auth_server(auth_server_id, "userfile", userfile)


def get_auth_url(self, portal_id):
    return self.config.get_from_portal("portal_id", "auth_url")


def get_auth_servers(self):
    auth_server_ids = self.config.get_auth_servers()
    auth_servers = []

    for auth_server_id in auth_server_ids:
        auth_servers += [{
            "id": auth_server_id,
            "connection": self.config.get_from_auth_server(auth_server_id, "connection"),
            "protocol": self.config.get_from_auth_server(auth_server_id, "protocol"),
            "url": self.config.get_from_auth_server(auth_server_id, "url"),
            "userfile": self.config.get_from_auth_server(auth_server_id, "userfile"),
        }]

    return auth_servers

def get_auth_server(self, auth_server_id):
    auth_servers = self.get_auth_servers()

    for auth_server in auth_servers:
        if auth_server["id"] == auth_server_id:
            return auth_server

    raise Exception("Authenication server not found")


def create_auth_server(self, auth_server_id, connection, auth_protocol, auth_url, userfile):
    self.config.create_auth_server(auth_server_id, connection, auth_protocol, auth_url, userfile)
    self.reload_from_config()

def auth_server_remove(self, auth_server_id):
    self.config.remove_section("auth_server." + auth_server_id)
    self.reload_from_config()

def get_single_auth_server_id(self):
    return self.config.get_single_auth_server_id()

def get_available_auth_server_implementations(self):
    return self.app.config["AUTH_SERVER_IMPLEMENTATIONS"]
