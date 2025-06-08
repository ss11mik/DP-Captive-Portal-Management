"""
Filename: settings.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login


def define_gui(app, application_layer):

    @app.route('/gui/settings/general', methods=['GET'])
    @flask_login.login_required
    def gui_settings_general():
        message = request.args.get("message", "", type=str)
        return render_template('settings_general.html', config=application_layer.get_config(), message=message, portals=application_layer.get_portals())

    @app.route('/gui/settings/general/admin', methods=['POST'])
    @flask_login.login_required
    def gui_settings_apply_admin():
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            return render_template('errors/error.html', message="Passwords do not match."), 400

        if password == "":
            return render_template('errors/error.html', message="Password cannot be empty."), 400

        if username == "":
            return render_template('errors/error.html', message="Username cannot be empty."), 400

        application_layer.apply_settings_admin(password, username)

        return redirect(url_for('gui_settings_general', message="Settings applied successfully."))

    @app.route('/gui/settings/single', methods=['POST'])
    @flask_login.login_required
    def gui_settings_apply_single():
        portal_id = request.form['portal']

        application_layer.apply_settings_captive(portal_id)

        return redirect(url_for('gui_pool'))


    @app.route('/gui/settings/general/mode', methods=['POST'])
    @flask_login.login_required
    def gui_settings_apply_cpm_mode():
        mode = request.form['mode']

        application_layer.apply_settings_mode(mode)

        return redirect(url_for('gui_settings_general', message="Settings applied successfully."))
