"""
Filename: _simple.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import re

from ._abstract import Abstract_Auth_Server

class Simple_Auth_Server(Abstract_Auth_Server):

    def __init__(self, url, connection, userfile):
        self.url = url
        self.connection = connection
        self.userfile = userfile

    def _format(self, username, user_id, password):
        return "\n{}:{}:{}".format(username, user_id, password)

    def get_users(self):
        users = self.connection.read_file(self.userfile).strip().split('\n')
        users2 = []

        for user in users:
            if user != "":
                users2 += [{
                    "username": user.split(':')[0],
                    "user_id": user.split(':')[1],
                    "password": user.split(':')[2],
                }]
        return users2

    def get_userfile(self):
        return self.connection.read_file(self.userfile).strip()

    def add_users(self, users):
        users2 = ""

        for user in users:
            try:
                users2 += self._format(user["username"], user["user_id"], user["password"])
            except:
                pass

        self.connection.append_file(self.userfile, users2)

    def set_users(self, userfile):
        self.connection.upload_file(userfile, self.userfile)

    def remove_users_by_username(self, regex):
        users = self.get_users()
        users2 = ""

        for user in users:
            if not re.match(regex, user["username"]):
                users2 += "\n{}:{}".format(user["username"], user["user_id"])

        self.connection.write_file(self.userfile, users2)


    def remove_users_by_id(self, regex):
        users = self.get_users()
        users2 = ""

        for user in users:
            if not re.match(regex, user["user_id"]):
                users2 += self._format(user["username"], user["user_id"], user["password"])

        self.connection.write_file(self.userfile, users2)

    def reset_user_password(self, user_id, new_password):
        users = self.get_users()
        users2 = ""

        for user in users:
            if user["user_id"] == user_id:
                users2 += self._format(user["username"], user["username"], new_password)
            else:
                users2 += self._format(user["username"], user["username"], user["password"])

        self.connection.write_file(self.userfile, users2)
