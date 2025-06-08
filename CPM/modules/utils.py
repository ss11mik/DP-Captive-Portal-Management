"""
Filename: utils.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""


class Utils:

    def __init__(self, app):
        self.app = app

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower(
            ) in self.app.config['ALLOWED_EXTENSIONS']
