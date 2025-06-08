"""
Filename: _status.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import traceback
import imgkit

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from paramiko.ssh_exception import NoValidConnectionsError

import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

from CPM.modules.utils import Utils


def get_single_portal_name(self):
    return self.config.get_single_portal()


def get_portal_provider(self, portal_id):
    return self.portals[portal_id].get_name()


def is_running(self, portal_id):
    try:
        return self.portals[portal_id].is_running()
    except Exception:
        traceback.print_exc()
        return False


def get_status(self, portal_id):
    try:
        return self.portals[portal_id].get_status()
    except NoValidConnectionsError:
        return "Cannot connect to the captive portal."
    except KeyError:
        return "Portal not found"
    except Exception:
        traceback.print_exc()
        return ""


def get_logfile(self, portal_id):
    try:
        # return '\n'.join(self.portals[portal_id].get_logfile_content()).split('\n')
        return self.portals[portal_id].get_logfile_content()
    except NoValidConnectionsError:
        return "Cannot connect to the captive portal."
    except KeyError:
        return "Portal not found"
    except Exception:
        traceback.print_exc()
        return ""

def stop(self, portal_id):
    return self.portals[portal_id].stop()


def start(self, portal_id):
    return self.portals[portal_id].start()
