"""
Filename: _RADIUS.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import re

from ._abstract import Abstract_Auth_Server

class FreeRADIUS_Auth_Server(Abstract_Auth_Server):

    def __init__(self, url, connection, userfile):
        self.url = url
        self.connection = connection
        self.userfile = userfile

    def _format(self, username, user_id, password):
        return '\n{}    Cleartext-Password := "{}"\n'.format(username, password)

    def _parse(self, line):
        line = line.strip()
        username = user_id = re.search("^.*    Cleartext-Password := ", line).group().replace("    Cleartext-Password := ", "")
        password = re.search('    Cleartext-Password := ".*"', line).group().replace('    Cleartext-Password := ""', "").replace('"', '')
        return username, user_id, password

    def get_users(self):
        lines = self.connection.read_file(self.userfile).strip().split('\n')
        users2 = []

        for line in lines:
            try:
                username, user_id, password = self._parse(line)
                users2 += [{
                    "username": username,
                    "user_id": user_id,
                    "password": password,
                }]
            except:
                # FreeRADIUS user config can contain other lines as well
                pass

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
        lines = self.connection.read_file(self.userfile).split('\n')
        lines2 = []

        for line in lines:
            try:
                username, _, _ = self._parse(line)
                if not re.match(regex, username):
                    lines2 += [line]
            except:
                # FreeRADIUS user config can contain other lines as well
                lines2 += [line]

        self.connection.write_file(self.userfile, '\n'.join(lines2))


    def remove_users_by_id(self, regex):
        lines = self.connection.read_file(self.userfile).split('\n')
        lines2 = []

        for line in lines:
            try:
                _, user_id, _ = self._parse(line)
                if not re.match(regex, user_id):
                    lines2 += [line]
            except:
                # FreeRADIUS user config can contain other lines as well
                lines2 += [line]

        self.connection.write_file(self.userfile, '\n'.join(lines2))

    def reset_user_password(self, user_id, new_password):
        lines = self.connection.read_file(self.userfile).split('\n')
        lines2 = []

        for line in lines:
            try:
                username, this_user_id, password = self._parse(line)
                if this_user_id == user_id:
                    lines2 += [self._format(username, this_user_id, new_password)]
                else:
                    lines2 += [line]
            except:
                # FreeRADIUS user config can contain other lines as well
                lines2 += [line]

        self.connection.write_file(self.userfile, '\n'.join(lines2))
