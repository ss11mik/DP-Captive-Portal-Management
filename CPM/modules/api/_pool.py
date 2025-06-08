"""
Filename: _pool.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

def define_api_endpoints(app, application_layer):

    @app.route('/api/pool')
    @flask_login.login_required
    def api_pool():
        """List captive portals available in CPM
        ---
        responses:
          200:
            description: List of captive portals
          401:
            description: Unauthorized
        """
        return application_layer.get_portals()

    @app.route('/api/pool/add/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def api_pool_add(portal_id):
        """Add captive portal to list of actively controlled
        ---
        parameters:
          - name: portal_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Settings of portals pool updated
          401:
            description: Unauthorized
        """
        application_layer.add_to_pool(portal_id)
        return "", 200

    @app.route('/api/pool/remove/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def api_pool_remove(portal_id):
        """Remove captive portal from list of actively controlled
        ---
        parameters:
          - name: portal_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Settings of portals pool updated
          401:
            description: Unauthorized
        """
        application_layer.remove_from_pool(portal_id)
        return "", 200

