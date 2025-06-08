"""
Filename: _connection.py
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


def apply_settings_connection(self, connection_id, connection_type, params):
    for key in params.keys():
        for value in params.getlist(key):
            self.config.set("connection." + connection_id, key, value)
    self.reload_from_config()


def remove_settings_connection(self, connection_id):
    self.config.remove_section("connection." + connection_id)
    self.reload_from_config()


def get_single_connection(self):
    return self.config.get_single_connection()


def get_connections(self):
    connection_ids = self.config.get_connections()
    connections = []

    for connection_id in connection_ids:
        connections += [{
            "id": connection_id,
            "connection_type": self.config.get_from_connection(connection_id, "connection_type"),
        }]

    return connections


def create_connection(self, connection_id, connection_type):
    self.config.create_connection(connection_id, connection_type)
    self.reload_from_config()
