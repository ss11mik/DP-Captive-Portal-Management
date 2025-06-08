"""
Filename: connection.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


class Connection():

    def __init__(self, config):
        raise NotImplementedError('Abstract method')

    def exec(self, command):
        raise NotImplementedError('Abstract method')

    def read_file(self, filename):
        raise NotImplementedError('Abstract method')

    def download_file(self, src, dest):
        raise NotImplementedError('Abstract method')

    def write_file(self, filename, content):
        raise NotImplementedError('Abstract method')

    def append_file(self, filename, content):
        raise NotImplementedError('Abstract method')

    def upload_file(self, src, dest):
        raise NotImplementedError('Abstract method')
