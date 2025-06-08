"""
Filename: portals.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login


def define_gui(app, application_layer):

    @app.route('/gui/configure/portal', methods=['GET'])
    @flask_login.login_required
    def gui_config_portal_single():
        return gui_settings_portal(application_layer.get_single_portal())

    @app.route('/gui/portals/list/<portal_id>', methods=['GET'])
    @flask_login.login_required
    def gui_settings_portal(portal_id):
        message = request.args.get("message", "", type=str)
        connections = application_layer.get_connections()
        auth_servers = application_layer.get_auth_servers()
        return render_template('config/settings_portal.html', portal_id=portal_id, config=application_layer.get_config(), connections=connections, auth_servers=auth_servers, message=message)

    @app.route('/gui/portals/list/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def gui_settings_apply_portal(portal_id):
        try:
            method = request.form['method']
        except:
            method = ""
        if method == "DELETE":
            application_layer.remove_settings_portal(portal_id)
            return redirect(url_for('gui_pool'))
        else:
            params = request.form

            application_layer.apply_settings_portal(portal_id, params)
            application_layer.apply_auth_to_portal(portal_id, params['auth_server'])

            return redirect(url_for('gui_settings_portal', portal_id=portal_id, message="Settings applied successfully."))
