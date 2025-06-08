"""
Filename: local.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import subprocess
import shutil
import fabric
import os

from .connection import Connection


class Local(Connection):

    def __init__(self, config):
        pass

    def exec(self, command, sudo=False):
        return subprocess.run(command, capture_output=True).stdout.decode('unicode_escape')


    def demote(self, user_uid, user_gid):
        def result():
            os.setgid(user_gid)
            os.setuid(user_uid)
        return result

    def exec_async(self, command, stdin=None, stderr=None, stdout=None, username=None, password=None):
        if password != None and username != None:
            proc = subprocess.Popen(command, stdin=stdin, stderr=stderr, stdout=stdout)

            proc.stdin.write(bytes('{}\n'.format(password), "utf8"))
            proc.stdin.flush()

        else:
            proc = subprocess.Popen(command, stdin=stdin, stderr=stderr, stdout=stdout)

        return proc

    def read_file(self, filename):
        with open(filename, 'r') as file:
            return file.read()

    def write_file(self, filename, content, sudo=False):
        with open(filename, 'w') as file:
            return file.write(content)

    def append_file(self, filename, content):
        with open(filename, 'a') as file:
            return file.write(content)

    def upload_file(self, src, dest):
        shutil.copy(src, dest)

    def download_file(self, src, dest):
        shutil.copy(src, dest)
