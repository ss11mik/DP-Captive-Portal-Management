"""
Filename: auth.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

from flask import render_template, request, redirect, url_for
import flask_login
from werkzeug.security import check_password_hash, generate_password_hash


def init(app):
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    with open(app.config['PASSWD_FILE'], 'r') as file:
        passwd = file.read().split('\n')

    users = {passwd[0]: {'password': passwd[1]}}

    class User(flask_login.UserMixin):
        pass

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return render_template('errors/unauthorized.html'), 401

    @login_manager.user_loader
    def user_loader(username):
        if username not in users:
            return

        user = User()
        user.id = username
        return user

    @login_manager.request_loader
    def request_loader(request):
        username = request.form.get('email')
        if username not in users:
            return

        user = User()
        user.id = username
        return user

    @app.route('/gui/login', methods=['GET'])
    def gui_login_page():
        return render_template('login.html')

    @app.route('/api/login', methods=['POST'])
    def api_login():
        """Log into CPM
        ---
        parameters:
          - name: username
            in: form
            type: string
            required: true
          - name: password
            in: form
            type: string
            required: true
        responses:
          200:
            description: Logged in
          401:
            description: Wrong username or password
        """
        username = request.form['username']
        if username in users and check_password_hash(users[username]['password'], request.form['password']):
            user = User()
            user.id = username
            flask_login.login_user(user)
            return "", 200

        return "", 401

    @app.route('/gui/login', methods=['POST'])
    def gui_login():
        username = request.form['username']
        if username in users and check_password_hash(users[username]['password'], request.form['password']):
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('gui_status'))

        return render_template('errors/error.html', message='Incorrect username or password'), 401

    @app.route('/api/logout')
    @flask_login.login_required
    def api_logout():
        """Log out of CPM
        ---
        responses:
          200:
            description: Logged out
        """
        flask_login.logout_user()
        return "", 200


    @app.route('/gui/logout')
    @flask_login.login_required
    def gui_logout():
        """Log out of CPM
        ---
        responses:
          200:
            description: Logged out
        """
        flask_login.logout_user()
        return render_template('errors/logged_out.html')


    return login_manager
