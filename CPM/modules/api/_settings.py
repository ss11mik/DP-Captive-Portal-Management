"""
Filename: _settings.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

def define_api_endpoints(app, application_layer):

    @app.route('/api/settings/admin', methods=['POST'])
    @flask_login.login_required
    def api_settings_apply_admin():
        """Set new administrator username and password
        ---
        parameters:
          - name: username
            in: form
            type: string
            required: true
          - name: password
            in: form
            type: string
            required: true
          - name: password2
            in: form
            type: string
            required: true
        responses:
          200:
            description: Settings updated
          401:
            description: Unauthorized
          404:
            description: Passwords do not match
        """
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            return "Passwords do not match.", 400

        if password == "":
            return "Password cannot be empty.", 400

        if username == "":
            return "Username cannot be empty.", 400

        application_layer.apply_settings_admin(password, username)

        return "", 200

    @app.route('/api/settings/single', methods=['POST'])
    @flask_login.login_required
    def api_settings_apply_single():
        """Set the captive portal used in single mode
        ---
        parameters:
          - name: portal
            in: form
            type: string
            required: true
        responses:
          200:
            description: Settings updated
          401:
            description: Unauthorized
        """
        portal_id = request.form['portal']

        application_layer.apply_settings_captive(portal_id)

        return "", 200


    @app.route('/api/settings/mode', methods=['POST'])
    @flask_login.login_required
    def api_settings_apply_cpm_mode():
        """Set the CPM mode
        ---
        parameters:
          - name: mode
            in: form
            type: string
            required: true
            description: either "single" or "pool"
        responses:
          200:
            description: Settings updated
          401:
            description: Unauthorized
        """
        mode = request.form['mode']

        application_layer.apply_settings_mode(mode)

        return "", 200

