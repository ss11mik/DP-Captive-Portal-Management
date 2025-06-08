"""
Filename: status.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import io
import time
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login


def define_gui(app, application_layer):

    @app.route('/')
    @app.route('/gui')
    @app.route('/gui/status')
    @flask_login.login_required
    def gui_status():
        if application_layer.get_settings_mode() == "single":
            return gui_status_single()

        elif application_layer.get_settings_mode() == "pool":
            return gui_status_pool()

    def gui_status_single():
        portal_id = application_layer.get_single_portal_name()
        status = ""
        is_running = application_layer.is_running(portal_id)

        if is_running:
            status = application_layer.get_status(portal_id)

        return render_template('status/status_single.html', portal_id=portal_id, is_running=is_running, status=status, portal_provider=application_layer.get_portal_provider(portal_id))

    def gui_status_pool():
        portals = application_layer.get_portals_for_status()
        return render_template('status/status_pool.html', portals=portals)

    @app.route('/gui/status/logs', methods=['GET'])
    @flask_login.login_required
    def gui_status_logs_single():
        portal_id = application_layer.get_single_portal_name()
        return gui_status_logs(portal_id)

    @app.route('/gui/status/logs/<portal_id>', methods=['GET'])
    @flask_login.login_required
    def gui_status_logs(portal_id):
        log = application_layer.get_logfile(portal_id)
        log_len = len(log.split('\n'))

        page = max(request.args.get("page", 0, type=int), 0)
        curent_page = request.args.get("curent-page", 0, type=int)
        per_page = request.args.get("per-page", 40, type=int)


        pagination_from = page
        pagination_to = page + per_page
        log = '\n'.join(log.split('\n')[pagination_from:pagination_to])

        return render_template('status/logs_pagination.html', portal_id=portal_id, log=log, curent_page=page, per_page=per_page, log_len=log_len)

    @app.route('/gui/status/stop', methods=['POST'])
    @flask_login.login_required
    def gui_status_stop_single():
        portal_id = application_layer.get_single_portal_name()
        return gui_status_stop(portal_id)

    @app.route('/gui/status/stop/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def gui_status_stop(portal_id):
        application_layer.stop(portal_id)
        return redirect(url_for('gui_status'))

    @app.route('/gui/status/start', methods=['POST'])
    @flask_login.login_required
    def gui_status_start_single():
        portal_id = application_layer.get_single_portal_name()
        return gui_status_start(portal_id)

    @app.route('/gui/status/start/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def gui_status_start(portal_id):
        application_layer.start(portal_id)
        time.sleep(.5)  # so it displays running after reload.
        return redirect(url_for('gui_status'))

    @app.route('/gui/logfile/download', methods=['GET'])
    @flask_login.login_required
    def gui_download_logfile_single():
        portal_id = application_layer.get_single_portal_name()
        return gui_download_logfile(portal_id)

    @app.route('/gui/logfile/download/<portal_id>', methods=['GET'])
    @flask_login.login_required
    def gui_download_logfile(portal_id):
        mem = io.BytesIO()
        try:
            mem.write(bytes(application_layer.get_logfile(portal_id), "utf8"))
        except TypeError:
            mem.write(bytes(''.join(application_layer.get_logfile(portal_id)), "utf8"))
        mem.seek(0)

        date = datetime.today().strftime('%Y-%m-%d')

        return send_file(
            mem,
            as_attachment=True,
            download_name='{}-{}.log'.format(portal_id, date),
            mimetype='text/plain'
        )
