"""
Filename: __init__.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import os
import traceback

from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login


import CPM.modules.auth
import CPM.modules.gui.nav
import CPM.modules.backend
import CPM.modules.swagger
from CPM.modules.application_layer import Application_layer
from CPM.modules.gui.gui import define_gui_endpoints
from CPM.modules.api import define_api_endpoints
import CPM.modules.configuration_file
from CPM.modules.utils import Utils


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)


# ensure the instance folder exists
try:
    os.makedirs(app.instance_path, exist_ok=True)
except OSError:
    traceback.print_exc()
    exit(1)


app.config.from_pyfile('config.py')

# initialize modules of the system
CPM.modules.auth.init(app)  # authentization
CPM.modules.swagger.init(app)   # Swagger (API documentation)


# the main configuration file
config = CPM.modules.configuration_file.CPM_config(app.config['CONFIG_FILE'])

_portals, _auth_servers = CPM.modules.backend.init_backends(app, config)
application_layer = Application_layer(app, _portals, _auth_servers, config)


CPM.modules.gui.nav.init(app, config)   # navigation menu

if app.config['API_ENABLED']:
    # define API endpoints
    define_api_endpoints(app, application_layer)

if app.config['GUI_ENABLED']:
    # define GUI (web) endpoints
    define_gui_endpoints(app, application_layer)

