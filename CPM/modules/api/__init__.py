"""
Filename: __init__.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

import CPM.modules.api._auth
import CPM.modules.api._connections
import CPM.modules.api._pool
import CPM.modules.api._portals
import CPM.modules.api._settings
import CPM.modules.api._status
import CPM.modules.api._themes
import CPM.modules.api._users


def define_api_endpoints(app, application_layer):

    CPM.modules.api._auth.define_api_endpoints(app, application_layer)
    CPM.modules.api._connections.define_api_endpoints(app, application_layer)
    CPM.modules.api._pool.define_api_endpoints(app, application_layer)
    CPM.modules.api._portals.define_api_endpoints(app, application_layer)
    CPM.modules.api._settings.define_api_endpoints(app, application_layer)
    CPM.modules.api._status.define_api_endpoints(app, application_layer)
    CPM.modules.api._themes.define_api_endpoints(app, application_layer)
    CPM.modules.api._users.define_api_endpoints(app, application_layer)



