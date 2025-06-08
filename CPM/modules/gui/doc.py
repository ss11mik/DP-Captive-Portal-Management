"""
Filename: doc.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login


def define_gui(app, application_layer):
    @app.route('/gui/doc')
    @flask_login.login_required
    def gui_doc():
        return render_template('doc.html')
