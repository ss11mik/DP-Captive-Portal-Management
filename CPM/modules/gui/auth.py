"""
Filename: auth.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login


def define_gui(app, application_layer):

    @app.route('/gui/auth', methods=['GET'])
    @flask_login.login_required
    def gui_config_auth_single():
        auth_server_id = application_layer.get_single_auth_server_id()
        if auth_server_id == "":
            return render_template('errors/error.html', message="Authentication Server is not configured for current captive portal.")
        return gui_config_auth(auth_server_id)

    @app.route('/gui/auth/list', methods=['GET'])
    @flask_login.login_required
    def gui_auth_servers_list():
        message = request.args.get("message", "", type=str)
        servers = application_layer.get_auth_servers()
        connections = application_layer.get_connections()
        auth_server_implementations = application_layer.get_available_auth_server_implementations()
        return render_template('auth_servers.html', servers=servers, message=message, connections=connections, auth_server_implementations=auth_server_implementations)

    @app.route('/gui/auth/list/<auth_server_id>', methods=['GET'])
    @flask_login.login_required
    def gui_config_auth(auth_server_id):
        message = request.args.get("message", "", type=str)
        server = application_layer.get_auth_server(auth_server_id)
        auth_server_implementations = application_layer.get_available_auth_server_implementations()
        return render_template('config/auth.html', config=application_layer.get_config(), message=message, server=server, auth_server_implementations=auth_server_implementations)


    @app.route('/gui/auth/list/<auth_server_id>', methods=['POST'])
    @flask_login.login_required
    def gui_auth_apply(auth_server_id):
        params = request.form
        application_layer.apply_auth(auth_server_id, params)
        return redirect(url_for('gui_config_auth', auth_server_id=auth_server_id, message="Settings applied successfully."))

    @app.route('/gui/auth/remove/<auth_server_id>', methods=['POST'])
    @flask_login.login_required
    def gui_auth_server_remove(auth_server_id):
        request.form
        application_layer.auth_server_remove(auth_server_id)
        return redirect(url_for('gui_auth_servers_list', message="Removed."))


    @app.route('/gui/auth/add', methods=['POST'])
    @flask_login.login_required
    def gui_authentication_add():
        auth_server_id = request.form['auth_server_id']
        connection = request.form['connection']
        protocol = request.form['protocol']
        url = request.form['url']
        userfile = request.form['userfile']

        application_layer.create_auth_server(auth_server_id, connection, protocol, url, userfile)

        return redirect(url_for('gui_auth_servers_list', message="New Authentication Server added."))
