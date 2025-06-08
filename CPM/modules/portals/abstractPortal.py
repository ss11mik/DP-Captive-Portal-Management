"""
Filename: abstractPortal.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

class AbstractPortal():

    def __init__(self, config):
        raise NotImplementedError('Abstract method')

    def get_name(self):
        raise NotImplementedError('Abstract method')

    def is_running(self):
        raise NotImplementedError('Abstract method')

    def start(self):
        raise NotImplementedError('Abstract method')

    def stop(self):
        raise NotImplementedError('Abstract method')

    def get_status(self):
        raise NotImplementedError('Abstract method')

    def get_applied_theme_id(self):
        raise NotImplementedError('Abstract method')

    def apply_theme(self, src):
        raise NotImplementedError('Abstract method')

    def get_logfile_content(self):
        raise NotImplementedError('Abstract method')

    def apply_auth(self, auth_protocol, auth_url, auth_timeout, auth_method):
        raise NotImplementedError('Abstract method')
