"""
Filename: pool.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login


def define_gui(app, application_layer):

    @app.route('/gui/pool')
    @flask_login.login_required
    def gui_pool():
        portals = application_layer.get_portals()
        connections = application_layer.get_connections()
        auth_servers = application_layer.get_auth_servers()
        portal_implementations = application_layer.get_available_captive_portal_implementations()
        return render_template('portals_pool.html', portals=portals, connections=connections, auth_servers=auth_servers, mode=application_layer.get_settings_mode(), portal_implementations=portal_implementations)

    @app.route('/gui/portal', methods=['POST'])
    @flask_login.login_required
    def gui_portal_add():
        portal_id = request.form['portal_id']
        implementation = request.form['implementation']
        connection = request.form['connection']
        auth_server = request.form['auth_server']

        application_layer.create_portal(portal_id, implementation, connection, auth_server)

        return redirect(url_for('gui_pool'))

    @app.route('/gui/portal/delete/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def gui_portal_remove(portal_id):
        method = request.form['method']
        if method == "DELETE":
            application_layer.remove_settings_portal(portal_id)

        return redirect(url_for('gui_pool'))

    @app.route('/gui/pool/add/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def gui_pool_add(portal_id):
        application_layer.add_to_pool(portal_id)
        return redirect(url_for('gui_pool'))

    @app.route('/gui/pool/remove/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def gui_pool_remove(portal_id):
        application_layer.remove_from_pool(portal_id)
        return redirect(url_for('gui_pool'))
