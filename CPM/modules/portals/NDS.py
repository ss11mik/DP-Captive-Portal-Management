"""
Filename: NDS.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import subprocess
import os
import sys

from .abstractPortal import AbstractPortal


class NDS(AbstractPortal):

    ndsctl_binary = "ndsctl"
    nodogsplash_binary = "nodogsplash"
    config_file = "nodogsplash.conf"
    resources_folder = "resources"
    log_filename = "nds.log"

    def __init__(self, config, connection):
        self.nodogsplash_binary = config['NDS_BINARY']
        self.ndsctl_binary = "ndsctl"
        self.config_file = config['NDS_CONFIG']
        self.resources_folder = config['NDS_RESOURCES']
        self.log_filename = os.path.join(config['NDS_RESOURCES'], "nds.log")

        self.connection = connection

    def get_name(self):
        return "NoDogSplash"

    def is_running(self):
        try:
            return self.get_status() != ""
        except Exception as e:
            print("Error reading state:" + str(e), file=sys.stderr)
            return False

    def start(self):
        # return self.connection.exec_async("{} -d 3 -f -r {} -c {} &>> {}".format(self.nodogsplash_binary, self.resources_folder, self.config_file, self.log_filename))
        return self.connection.exec_async("{}/run.sh".format(self.resources_folder))

    def stop(self):
        try:
            return self.connection.exec("sudo {} stop".format(self.ndsctl_binary))
        except Exception as e:
            raise Exception("Error reading state:" + str(e))

    def get_status(self):
        try:
            return self.connection.exec('sudo {} status || exit 0'.format(self.ndsctl_binary)).stdout
        except Exception as e:
            raise Exception("Error reading state:" + str(e))

    def get_applied_theme_id(self):
        return self.connection.read_file(os.path.join(self.resources_folder, 'theme_id')).rstrip('\n')

    def apply_theme(self, src):
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if os.path.isfile(full_file_name):
                self.connection.upload_file(
                    full_file_name, self.resources_folder)


    def apply_auth(self, auth_protocol, auth_url, auth_timeout, auth_method, radius_secret="", ldap_query=""):
        for file_name, file_content in [
            ("auth_protocol.conf", auth_protocol),
            ("auth_url.conf", auth_url),
            ("auth_timeout.conf", auth_timeout),
            ("auth_method.conf", auth_method),
            ("radius_secret.conf", radius_secret),
            ("ldap_query.conf", ldap_query)
            ]:
            self.connection.write_file(
                os.path.join(self.resources_folder, "CPM_auth", file_name), file_content)


    def get_logfile_content(self):
        return self.connection.read_file(self.log_filename)
