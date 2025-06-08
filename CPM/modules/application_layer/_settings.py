"""
Filename: _settings.py
Author: Bc. Ondřej Mikula @ FIT BUT
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


def apply_settings_admin(self, password, username):

    password_hash = generate_password_hash(password)

    with open(self.app.config['PASSWD_FILE'], 'w') as file:
        file.write("{}\n{}".format(username, password_hash))

    users = {username: {'password': password_hash}}


def apply_settings_captive(self, portal_id):
    try:
        self.config.get("portal." + portal_id, "implementation")
    except:
        raise Exception("Portal with specified ID does not exist.")

    self.config.set("mode.single", "portal", portal_id)


def apply_settings_mode(self, mode):
    self.config.set("mode", "mode", mode)


def get_settings_mode(self):
    return self.config.get("mode", "mode")
