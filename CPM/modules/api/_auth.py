"""
Filename: _auth.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

def define_api_endpoints(app, application_layer):

    @app.route('/api/auth', methods=['GET'])
    @flask_login.login_required
    def api_auth_servers_list():
        """List authentication servers available in CPM
        ---
        responses:
          200:
            description: List of authentication servers
          401:
            description: Unauthorized
        """
        servers = application_layer.get_auth_servers()
        return servers

    @app.route('/api/auth/<auth_server_id>', methods=['GET'])
    @flask_login.login_required
    def api_config_auth(auth_server_id):
        """Get details of authentication server
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Details of authentication server
          401:
            description: Unauthorized
        """
        server = application_layer.get_auth_server(auth_server_id)
        return server

    @app.route('/api/auth/<auth_server_id>', methods=['POST'])
    @flask_login.login_required
    def api_auth_apply(auth_server_id):
        """Apply settings to authentication server
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
          - name: protocol
            in: form
            type: string
            required: true
          - name: url
            in: form
            type: string
            required: true
          - name: userfile
            in: form
            type: string
            required: true
        responses:
          200:
            description: Settings applied
          401:
            description: Unauthorized
        """
        params = request.form
        application_layer.apply_auth(auth_server_id, params)
        return "", 200

    @app.route('/api/auth/<auth_server_id>', methods=['DELETE'])
    @flask_login.login_required
    def api_auth_server_remove(auth_server_id):
        """Delete authentication server from CPM
        ---
        parameters:
          - name: portal_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Authentication server deleted
          401:
            description: Unauthorized
        """
        request.form
        application_layer.auth_server_remove(auth_server_id)
        return "", 200


    @app.route('/api/auth', methods=['PUT'])
    @flask_login.login_required
    def api_authentication_add():
        """Add new authentication server to CPM
        ---
        parameters:
          - name: auth_server_id
            in: form
            type: string
            required: true
          - name: protocol
            in: form
            type: string
            required: true
          - name: url
            in: form
            type: string
            required: true
          - name: userfile
            in: form
            type: string
            required: true
        responses:
          200:
            description: Authentication server added to CPM
          401:
            description: Unauthorized
        """
        auth_server_id = request.form['auth_server_id']
        connection = request.form['connection']
        protocol = request.form['protocol']
        url = request.form['url']
        userfile = request.form['userfile']

        application_layer.create_auth_server(auth_server_id, connection, protocol, url, userfile)

        return "", 200
