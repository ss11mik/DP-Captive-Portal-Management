"""
Filename: gui.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import traceback
import os

from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request, send_from_directory
import flask_login

import CPM.modules.gui.themes
import CPM.modules.gui.status
import CPM.modules.gui.pool
import CPM.modules.gui.connections
import CPM.modules.gui.settings
import CPM.modules.gui.users
import CPM.modules.gui.doc
import CPM.modules.gui.auth
import CPM.modules.gui.portals


def define_gui_endpoints(app, application_layer):

    CPM.modules.gui.themes.define_gui(app, application_layer)
    CPM.modules.gui.status.define_gui(app, application_layer)
    CPM.modules.gui.pool.define_gui(app, application_layer)
    CPM.modules.gui.settings.define_gui(app, application_layer)
    CPM.modules.gui.users.define_gui(app, application_layer)
    CPM.modules.gui.doc.define_gui(app, application_layer)
    CPM.modules.gui.auth.define_gui(app, application_layer)
    CPM.modules.gui.connections.define_gui(app, application_layer)
    CPM.modules.gui.portals.define_gui(app, application_layer)


    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')


    @app.errorhandler(Exception)
    def handle_exception(e):
        traceback.print_exc()
        return render_template('errors/error.html', message="Error: " + str(e)), 400
