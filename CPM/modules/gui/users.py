"""
Filename: users.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login

import io
from datetime import datetime
import traceback


def define_gui(app, application_layer):

    @app.route('/gui/users', methods=['GET'])
    @flask_login.login_required
    def gui_list_users_single():
        return gui_list_users(application_layer.get_single_auth_server())

    @app.route('/gui/users/<auth_server_id>', methods=['GET'])
    @flask_login.login_required
    def gui_list_users(auth_server_id):
        users = application_layer.get_auth_server_users(auth_server_id)
        return render_template('users.html', auth_server_id=auth_server_id, users=users)



    @app.route('/gui/users/<auth_server_id>/reset/<user_id>', methods=['POST'])
    @flask_login.login_required
    def gui_users_reset_password(auth_server_id, user_id):
        application_layer.reset_user_password(auth_server_id, user_id, request.form['new_password'])
        return redirect(url_for('gui_list_users', auth_server_id=auth_server_id))

    @app.route('/gui/users/<auth_server_id>/remove/id', methods=['POST'])
    @flask_login.login_required
    def gui_users_remove_user_by_id(auth_server_id):
        application_layer.remove_users_by_id(auth_server_id, request.form['regex'])
        return redirect(url_for('gui_list_users', auth_server_id=auth_server_id))

    @app.route('/gui/users/<auth_server_id>/remove/username', methods=['POST'])
    @flask_login.login_required
    def gui_users_remove_user_by_username(auth_server_id):
        application_layer.remove_users_by_username(auth_server_id, request.form['regex'])
        return redirect(url_for('gui_list_users', auth_server_id=auth_server_id))

    @app.route('/gui/users/<auth_server_id>/add/file', methods=['POST'])
    @flask_login.login_required
    def gui_users_add_users(auth_server_id):
        try:
            application_layer.add_users_from_file(auth_server_id, request.files['userfile'])
            return redirect(url_for('gui_list_users', auth_server_id=auth_server_id))
        except:
            traceback.print_exc()
            return render_template('errors/error.html', message="Could not add users."), 400


    @app.route('/gui/users/<auth_server_id>/add/single', methods=['POST'])
    @flask_login.login_required
    def gui_users_add_user(auth_server_id):
        try:
            user = {
                "username": request.form['username'],
                "user_id": request.form['user_id'],
                "password": request.form['password'],
            }
            application_layer.add_users(auth_server_id, [user])
            return redirect(url_for('gui_list_users', auth_server_id=auth_server_id))
        except:
            traceback.print_exc()
            return render_template('errors/error.html', message="Could not add user."), 400


    @app.route('/gui/users/<auth_server_id>/backup', methods=['POST'])
    @flask_login.login_required
    def gui_users_backup(auth_server_id):
        users = application_layer.get_userfile(auth_server_id)

        mem = io.BytesIO()
        if type(users) == str:
            mem.write(bytes(users, "utf8"))
        else:
            mem.write(users)
        mem.seek(0)

        date = datetime.today().strftime('%Y-%m-%d')

        return send_file(
            mem,
            as_attachment=True,
            download_name='{}-{}.backup'.format(auth_server_id, date),
            mimetype='text/plain'
        )

    @app.route('/gui/users/<auth_server_id>/restore', methods=['POST'])
    @flask_login.login_required
    def gui_users_restore(auth_server_id):
        try:
            application_layer.restore_users(auth_server_id, request.files['userfile'])
            return redirect(url_for('gui_list_users', auth_server_id=auth_server_id))
        except:
            traceback.print_exc()
            return render_template('errors/error.html', message="Could not restore users."), 400
