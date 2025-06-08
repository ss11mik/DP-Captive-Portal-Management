"""
Filename: _portals.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

def define_api_endpoints(app, application_layer):

    @app.route('/api/portal', methods=['PUT'])
    @flask_login.login_required
    def api_portal_add():
        """Add a new portal to CPM
        ---
        parameters:
          - name: portal_id
            in: path
            type: string
            required: true
          - name: implementation
            in: form
            type: string
            required: true
          - name: connection
            in: form
            type: string
            required: true
          - name: auth_server
            in: form
            type: string
            required: true
        responses:
          200:
            description: Portal added
          401:
            description: Unauthorized
        """
        portal_id = request.form['portal_id']
        implementation = request.form['implementation']
        connection = request.form['connection']
        auth_server = request.form['auth_server']

        application_layer.create_portal(portal_id, implementation, connection, auth_server)

        return "", 200

    @app.route('/api/portals/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def api_apply_portal(portal_id):
        """Apply settings to captive portal
        ---
        parameters:
          - name: portal_id
            in: path
            type: string
            required: true
          - name: implementation
            in: form
            type: string
            required: true
          - name: connection
            in: form
            type: string
            required: true
          - name: auth_server
            in: form
            type: string
            required: true
          - name: pfsense_config
            in: form
            type: string
            required: false
          - name: nds_folder
            in: form
            type: string
            required: false
          - name: nds_binary
            in: form
            type: string
            required: false
          - name: nds_config
            in: form
            type: string
            required: false
          - name: nds_resources
            in: form
            type: string
            required: false
        responses:
          200:
            description: Settings updated
          401:
            description: Unauthorized
        """
        params = request.form
        application_layer.apply_settings_portal(portal_id, params)
        return "", 200

    @app.route('/api/portals/<portal_id>', methods=['DELETE'])
    @flask_login.login_required
    def api_delete_portal(portal_id):
        """Delete a captive portal from CPM
        ---
        parameters:
          - name: portal_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Portal deleted
          401:
            description: Unauthorized
        """
        application_layer.remove_settings_portal(portal_id)
        return "", 200

