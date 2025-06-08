"""
Filename: connections.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login


def define_gui(app, application_layer):

    @app.route('/gui/connections')
    @flask_login.login_required
    def gui_connections():
        connections = application_layer.get_connections()
        return render_template('connections.html', connections=connections)

    @app.route('/gui/connections/single')
    @flask_login.login_required
    def gui_connections_single():
        connection_id = application_layer.get_single_connection()
        if connection_id == "":
            return render_template('errors/error.html', message="Connection is not configured for current captive portal.")
        return gui_settings_connection(connection_id)

    @app.route('/gui/connections/edit/<connection_id>', methods=['GET'])
    @flask_login.login_required
    def gui_settings_connection(connection_id):
        message = request.args.get("message", "", type=str)
        return render_template('config/settings_connection.html', connection_id=connection_id, config=application_layer.get_config(), message=message)

    @app.route('/gui/connections/apply/<connection_id>', methods=['POST'])
    @flask_login.login_required
    def gui_settings_apply_connection(connection_id):
        connection_type = request.form['connection_type']
        params = request.form

        application_layer.apply_settings_connection(
            connection_id, connection_type, params)

        return redirect(url_for('gui_settings_connection', connection_id=connection_id, message="Settings applied successfully."))


    @app.route('/gui/connections/add', methods=['POST'])
    @flask_login.login_required
    def gui_connection_add():
        connection_id = request.form['connection_id']
        connection_type = request.form['connection_type']

        application_layer.create_connection(connection_id, connection_type)

        return redirect(url_for('gui_connections'))

    @app.route('/gui/connections/delete/<connection_id>', methods=['POST'])
    @flask_login.login_required
    def gui_connection_remove(connection_id):
        method = request.form['method']
        if method == "DELETE":
            application_layer.remove_settings_connection(connection_id)

        return redirect(url_for('gui_connections'))
