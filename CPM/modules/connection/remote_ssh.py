"""
Filename: remote_ssh.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import fabric
from paramiko import RSAKey
import io

from .connection import Connection


class Remote_SSH(Connection):

    def __init__(self, config):
        self.host = config['remote_host']
        self.port = config['remote_port']
        self.username = config['remote_username']
        self.keyfile = config['remote_keyfile']
        self.password = config['remote_password']
        self.auth_method = config['remote_auth_method']

        if  self.auth_method == "password":
            pass
        elif  self.auth_method == "keyfile":
            pass
        else:
            raise Exception("Unknown authentication method specified: " + self.auth_method)

    def create_connection(self):
        if  self.auth_method == "password":
            return fabric.Connection(host=self.host, port=self.port, user=self.username, connect_kwargs={
                                   'password': self.password})
        elif  self.auth_method == "keyfile":
            return fabric.Connection(host=self.host, port=self.port, user=self.username, connect_kwargs={
                                   'pkey': RSAKey.from_private_key_file(self.keyfile)})

    def exec(self, command, sudo=False):
        with self.create_connection() as connection:
            if sudo:
                return connection.sudo(command)
            else:
                return connection.run(command)

    def exec_async(self, command, stdin=None, stderr=None, stdout=None, sudo=False):
        with self.create_connection() as connection:
            if sudo:
                return connection.sudo(command, disown=True)
            else:
                return connection.run(command, disown=True)

    def read_file(self, filename):
        with self.create_connection() as connection:
            return connection.run("cat \"{}\"".format(filename)).stdout

    def write_file(self, filename, content, sudo=False):
        with self.create_connection() as connection:
            in_stream = io.StringIO(content)
            connection.put(in_stream, filename)
            # if sudo:
            #     return connection.sudo("cat > {}".format(filename), in_stream=in_stream)
            # else:
            #     return connection.run("cat > {}".format(filename), in_stream=in_stream)

    def append_file(self, filename, content):
        with self.create_connection() as connection:
            in_stream = io.StringIO(content)
            return connection.run("cat >> {}".format(filename), in_stream=in_stream)

    def upload_file(self, src, dest, sudo=False):
        with self.create_connection() as connection:
            connection.put(src, dest)

    def download_file(self, src, dest):
        with self.create_connection() as connection:
            connection.get(src, dest)
