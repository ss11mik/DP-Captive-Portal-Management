"""
Filename: _themes.py
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


def upload_theme(self, theme_file):
    if theme_file.filename == "":
        return redirect(request.url)
    if theme_file and self.utils.allowed_file(theme_file.filename):
        @after_this_request
        def delete_tmpzip(response):
            try:
                os.remove(os.path.join(
                    self.app.config['TMP_FOLDER'], filename))
            except Exception:
                traceback.print_exc()
            return response

        filename = secure_filename(theme_file.filename)
        theme_file.save(os.path.join(self.app.config['TMP_FOLDER'], filename))
        shutil.unpack_archive(os.path.join(self.app.config['TMP_FOLDER'], filename), os.path.join(
            self.app.config['THEMES_FOLDER'], filename.split('.', 1)[0]))


def apply_theme(self, portal_id, src_dir):
    self.portals[portal_id].apply_theme(src_dir)


def scrape_theme(self, splash_url, status_url, theme_id, auth_method):
    # create firectory for the new theme
    directory = os.path.join(
        self.app.config['THEMES_FOLDER'], secure_filename(theme_id))

    if os.path.isdir(directory):
        raise Exception("Theme already exists")
    os.makedirs(directory)

    # create id file
    with open(os.path.join(directory, "theme_id"), 'w') as file:
        file.write(theme_id)

    with open(os.path.join(directory, "auth_method"), 'w') as file:
        file.write(auth_method)

    scrape_cmd = "monolith -o {} {}".format(
        os.path.join(directory, 'splash.html'), splash_url).split(' ')

    result = subprocess.run(scrape_cmd, capture_output=True)
    if result.returncode != 0:
        shutil.rmtree(directory)
        raise Exception(result.stderr.decode('unicode_escape'))


    scrape_cmd = "monolith -o {} {}".format(
        os.path.join(directory, 'status.html'), status_url).split(' ')
    result = subprocess.run(scrape_cmd, capture_output=True)
    if result.returncode != 0:
        shutil.rmtree(directory)
        raise Exception(result.stderr.decode('unicode_escape'))


    # render the preview.
    try:
        imgkit.from_file(os.path.join(directory, 'splash.html'), os.path.join(
            directory, 'preview.png'), options={'crop-h': '1024', 'crop-w': '1024'})
    except OSError:
        # Ignore any errors from wkhtmltopdf as is throws them even for non-critical failures
        pass


def delete_theme(self, theme_id):
    shutil.rmtree('instance/themes/' + theme_id)


def prepare_theme_for_download(self, theme_id):
    zipfile_fname = os.path.join(
        self.app.config['TMP_FOLDER'], theme_id + '.zip')
    shutil.make_archive(os.path.join(self.app.config['TMP_FOLDER'], theme_id), 'zip', os.path.join(
        self.app.config['THEMES_FOLDER'], theme_id))
    return zipfile_fname


def list_themes(self):
    return os.listdir('instance/themes/')

def get_theme_auth_method(self, theme_id):
    with open(os.path.join(self.app.config['THEMES_FOLDER'], theme_id, "auth_method"), "r") as auth_method:
        return auth_method.read().strip()


def get_applied_theme_id(self, portal_id):
    try:
        return self.portals[portal_id].get_applied_theme_id()
    except Exception:
        return ""


def get_theme_preview(self, theme_id):
    return os.path.join(self.app.config['THEMES_FOLDER'], theme_id, 'preview.png')
