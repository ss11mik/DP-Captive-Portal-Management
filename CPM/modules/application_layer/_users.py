"""
Filename: _users.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


import os
import shutil
import subprocess
import imgkit
import traceback

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

from CPM.modules.utils import Utils


def get_auth_server_users(self, auth_server_id):
    try:
        return self.auth_servers[auth_server_id].get_users()
    except:
        return []

def get_userfile(self, auth_server_id):
    return self.auth_servers[auth_server_id].get_userfile()

def restore_users(self, auth_server_id, userfile):
    @after_this_request
    def delete_tmpfile(response):
        try:
            os.remove(abs_filename)
        except Exception:
            traceback.print_exc()
        return response

    filename = secure_filename(userfile.filename)
    abs_filename = os.path.join(self.app.config['TMP_FOLDER'], filename)
    userfile.save(abs_filename)
    return self.auth_servers[auth_server_id].set_users(abs_filename)

def remove_users_by_username(self, auth_server_id, regex):
    return self.auth_servers[auth_server_id].remove_users_by_username(regex)

def remove_users_by_id(self, auth_server_id, regex):
    return self.auth_servers[auth_server_id].remove_users_by_id(regex)

def add_users_from_file(self, auth_server_id, userfile):
    @after_this_request
    def delete_tmpfile(response):
        try:
            os.remove(abs_filename)
        except Exception:
            traceback.print_exc()
        return response

    filename = secure_filename(userfile.filename)
    abs_filename = os.path.join(self.app.config['TMP_FOLDER'], filename)
    userfile.save(abs_filename)

    users = ""
    with open(abs_filename, 'r') as file:
        users = file.read().split('\n')

    users2 = []
    for user in users:
        try:
            users2 += [{
                    "username": user.split(':')[0],
                    "user_id": user.split(':')[1],
                    "password": user.split(':')[2],
                }]
        except:
            pass

    return self.add_users(auth_server_id, users2)

def add_users(self, auth_server_id, users):
    return self.auth_servers[auth_server_id].add_users(users)

def reset_user_password(self, auth_server_id, user_id, new_password):
    return self.auth_servers[auth_server_id].reset_user_password(user_id, new_password)
