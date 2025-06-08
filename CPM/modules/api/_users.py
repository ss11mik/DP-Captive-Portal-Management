"""
Filename: _users.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

def define_api_endpoints(app, application_layer):

    @app.route('/api/users/<auth_server_id>', methods=['GET'])
    @flask_login.login_required
    def api_list_users(auth_server_id):
        """List users in authentication server
           May be slow or time out, includes connecting to the authentication server.
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: List of users
          401:
            description: Unauthorized
        """
        return application_layer.get_auth_server_users(auth_server_id)

    @app.route('/api/users/<auth_server_id>/reset/<user_id>', methods=['POST'])
    @flask_login.login_required
    def api_users_reset_password(auth_server_id, user_id):
        """Reset password of given user in authentication server
           May be slow or time out, includes connecting to the authentication server.
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
          - name: user_id
            in: path
            type: string
            required: true
          - name: new_password
            in: form
            type: string
            required: true
        responses:
          200:
            description: Password was reset
          401:
            description: Unauthorized
        """
        application_layer.reset_user_password(auth_server_id, user_id, request.form['new_password'])
        return "", 200

    @app.route('/api/users/<auth_server_id>/remove/id', methods=['POST'])
    @flask_login.login_required
    def api_users_remove_user_by_id(auth_server_id):
        """Remove users from authentication server by user ID
           May be slow or time out, includes connecting to the authentication server.
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
          - name: regex
            in: form
            type: string
            required: true
            description: Regular expression matching IDs of users to be removed.
        responses:
          200:
            description: Specified users removed
          401:
            description: Unauthorized
        """
        application_layer.remove_users_by_id(auth_server_id, request.form['regex'])
        return "", 200

    @app.route('/api/users/<auth_server_id>/remove/username', methods=['POST'])
    @flask_login.login_required
    def api_users_remove_user_by_username(auth_server_id):
        """Remove users from authentication server by username
           May be slow or time out, includes connecting to the authentication server.
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
          - name: regex
            in: form
            type: string
            required: true
            description: Regular expression matching usernames of users to be removed.
        responses:
          200:
            description: Specified users removed
          401:
            description: Unauthorized
        """
        application_layer.remove_users_by_username(auth_server_id, request.form['regex'])
        return "", 200

    @app.route('/api/users/<auth_server_id>/add/file', methods=['POST'])
    @flask_login.login_required
    def api_users_add_users(auth_server_id):
        """Add users to authentication server
           May be slow or time out, includes connecting to the authentication server.
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
          - name: userfile
            in: form
            type: file
            required: true
            description: A CSV file in format username:user_id:password.
        responses:
          200:
            description: Users added
          401:
            description: Unauthorized
        """
        try:
            application_layer.add_users_from_file(auth_server_id, request.files['userfile'])
            return "", 200
        except:
            traceback.print_exc()
            return "Could not add users.", 400


    @app.route('/api/users/<auth_server_id>/add/single', methods=['POST'])
    @flask_login.login_required
    def api_users_add_user(auth_server_id):
        """Add user to authentication server
           May be slow or time out, includes connecting to the authentication server.
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
          - name: username
            in: form
            type: string
            required: true
          - name: user_id
            in: form
            type: string
            required: true
          - name: password
            in: form
            type: string
            required: true
        responses:
          200:
            description: User added
          401:
            description: Unauthorized
        """
        try:
            user = {
                "username": request.form['username'],
                "user_id": request.form['user_id'],
                "password": request.form['password'],
            }
            application_layer.add_users(auth_server_id, [user])
            return "", 200
        except:
            traceback.print_exc()
            return "Could not add user.", 400

    @app.route('/api/users/<auth_server_id>/backup', methods=['GET'])
    @flask_login.login_required
    def api_users_backup(auth_server_id):
        """Backup user database from authentication server
           May be slow or time out, includes connecting to the authentication server.
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: User database in format dependent on specific authentication server implementation
          401:
            description: Unauthorized
        """
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

    @app.route('/api/users/<auth_server_id>/restore', methods=['POST'])
    @flask_login.login_required
    def api_users_restore(auth_server_id):
        """Restore user database from backup
           May be slow or time out, includes connecting to the authentication server.
        ---
        parameters:
          - name: auth_server_id
            in: path
            type: string
            required: true
          - name: userfile
            in: form
            type: file
            required: true
            description: User database in format dependent on specific authentication server implementation
        responses:
          200:
            description: Database restored
          401:
            description: Unauthorized
        """
        try:
            application_layer.restore_users(auth_server_id, request.files['userfile'])
            return "", 200
        except:
            traceback.print_exc()
            return "Could not restore users.", 400
