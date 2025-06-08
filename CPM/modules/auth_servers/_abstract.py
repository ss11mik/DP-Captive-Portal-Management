"""
Filename: Abstract_Auth_Server.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


class Abstract_Auth_Server:

    def __init__(self, url, connection, userfile):
        raise NotImplementedError('Abstract method')

    def _format(username, user_id, password):
        raise NotImplementedError('Abstract method')

    def get_users(self):
        raise NotImplementedError('Abstract method')

    def get_userfile(self):
        raise NotImplementedError('Abstract method')

    def add_users(self, users):
        raise NotImplementedError('Abstract method')

    def set_users(self, userfile):
        raise NotImplementedError('Abstract method')

    def remove_users_by_username(self, regex):
        raise NotImplementedError('Abstract method')

    def remove_users_by_id(self, regex):
        raise NotImplementedError('Abstract method')

    def reset_user_password(self, user_id, new_password):
        raise NotImplementedError('Abstract method')

