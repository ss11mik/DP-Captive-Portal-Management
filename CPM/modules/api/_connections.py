"""
Filename: _connections.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

def define_api_endpoints(app, application_layer):

    @app.route('/api/connections')
    @flask_login.login_required
    def api_connections():
        """List connections available in CPM
        ---
        responses:
          200:
            description: List of connections
          401:
            description: Unauthorized
        """
        return application_layer.get_connections()

    @app.route('/api/connections/apply/<connection_id>', methods=['POST'])
    @flask_login.login_required
    def api_settings_apply_connection(connection_id):
        """Change configuration of conection
        ---
        parameters:
          - name: connection_id
            in: path
            type: string
            required: true
          - name: connection_type
            in: form
            type: string
            required: true
        responses:
          200:
            description: Settings of portals pool updated
          401:
            description: Unauthorized
        """
        connection_type = request.form['connection_type']
        params = request.form

        application_layer.apply_settings_connection(
            connection_id, connection_type, params)

        return "", 200


    @app.route('/api/connections/add', methods=['POST'])
    @flask_login.login_required
    def api_connection_add():
        """Add new connection to CPM
        ---
        parameters:
          - name: connection_id
            in: form
            type: string
            required: true
          - name: connection_type
            in: form
            type: string
            required: true
        responses:
          200:
            description: New connection added
          401:
            description: Unauthorized
        """
        connection_id = request.form['connection_id']
        connection_type = request.form['connection_type']

        application_layer.create_connection(connection_id, connection_type)

        return "", 200

    @app.route('/api/connections/delete/<connection_id>', methods=['DELETE'])
    @flask_login.login_required
    def api_connection_remove(connection_id):
        """Remove connection from CPM
        ---
        parameters:
          - name: connection_id
            in: form
            type: string
            required: true
        responses:
          200:
            description: Connection removed
          401:
            description: Unauthorized
        """
        application_layer.remove_settings_connection(connection_id)

        return "", 200
