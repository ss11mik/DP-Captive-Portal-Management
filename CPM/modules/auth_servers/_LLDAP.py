"""
Filename: _LDAP.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import re
import sqlite3
import os
import traceback
from datetime import datetime
import uuid
from argon2 import PasswordHasher

from flask import after_this_request

from ._abstract import Abstract_Auth_Server

class LLDAP_Auth_Server(Abstract_Auth_Server):

    def __init__(self, url, connection, userfile, tmp_folder):
        self.url = url
        self.connection = connection
        self.userfile = userfile
        self.tmp_folder = tmp_folder
        self.tmp_sql_db_copy = os.path.join(self.tmp_folder, "ldap.db")


    def _execute_sql(self, commands, commit=False):
        """
        This method downloads copy of the SQL database with users into temporary folder of CPM.
        This way, transparent solution for both local and remote access can be achieved.
        """
        @after_this_request
        def delete_tmpzip(response):
            try:
                os.remove(self.tmp_sql_db_copy)
            except Exception:
                traceback.print_exc()
            return response


        self.connection.download_file(self.userfile, self.tmp_sql_db_copy)
        con = sqlite3.connect(self.tmp_sql_db_copy)
        cur = con.cursor()
        result = ""
        for command in commands:
            print(command)
            res = cur.execute(command)
            result = res.fetchall()

        if commit:
            con.commit()
            self.connection.upload_file(self.tmp_sql_db_copy, self.userfile)

        return result


    def _parse(self, line):
        username = line[7]
        user_id = line[0]
        password = line[3]
        return username, user_id, password

    def get_users(self):

        users = self._execute_sql(["SELECT * FROM users;"])
        users2 = []

        for user in users:
            username, user_id, password = self._parse(user)
            users2 += [{
                "username": username,
                "user_id": user_id,
                "password": password
            }]
        return users2

    def get_userfile(self):
        @after_this_request
        def delete_tmpzip(response):
            try:
                os.remove(self.tmp_sql_db_copy)
            except Exception:
                traceback.print_exc()
            return response

        self.connection.download_file(self.userfile, self.tmp_sql_db_copy)
        with open(self.tmp_sql_db_copy, 'rb') as file:
            return file.read()

    def add_users(self, users):
        commands = []

        ph = PasswordHasher()

        for user in users:
            password_hash = ph.hash(user["password"])
            commands += ['INSERT INTO users (user_id, email, creation_date, uuid, password_hash, display_name, lowercase_email) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(
                user["user_id"],
                "{}@vut.cz".format(user["user_id"]),    # email, as it is required
                datetime.now(),     # creation_date
                str(uuid.uuid4()),  # random UUID
                password_hash,
                user["username"],
                user["user_id"].lower(),    # lowercase email, as it is required
            )]

        self._execute_sql(commands, commit=True)

    def set_users(self, userfile):
        self.connection.upload_file(userfile, self.userfile)

    def remove_users_by_username(self, regex):
        self._execute_sql(['DELETE FROM users WHERE display_name LIKE "{}"'.format(regex)], commit=True)


    def remove_users_by_id(self, regex):
        self._execute_sql(['DELETE FROM users WHERE user_id LIKE "{}"'.format(regex)], commit=True)

    def reset_user_password(self, user_id, new_password):
        ph = PasswordHasher()
        password_hash = ph.hash(new_password)
        self._execute_sql(['UPDATE users SET password_hash = "{}" WHERE user_id LIKE "{}"'.format(password_hash, user_id)], commit=True)

