"""
Filename: pfSense.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

from bs4 import BeautifulSoup
import base64
import os
import sys

from .abstractPortal import AbstractPortal


class pfSense(AbstractPortal):

    def __init__(self, config, connection):
        self.config_filename = config['pfsense_config']
        self.log_filename = "/var/log/portalauth.log"
        # self.log_file = open("pfsense.log", 'a')

        self.connection = connection

    def get_name(self):
        return "pfSense"

    def __read_config(self):
        x = self.connection.read_file(self.config_filename)
        self.config = BeautifulSoup(x, "xml")
        self.captive_portal = self.config.find("captiveportal")

    def __apply_config(self):
        self.connection.write_file(
            self.config_filename, str(self.config), sudo=True)
        self.connection.exec("/etc/rc.reload_all")

    def is_running(self):
        try:
            self.__read_config()
            return self.captive_portal.find("enable") != None
        except Exception as e:
            print("Error reading state:" + str(e), file=sys.stderr)
            return False

    def start(self):
        if not self.is_running():
            new_tag = self.config.new_tag("enable")
            self.captive_portal.insert(0, new_tag)
            self.__apply_config()

    def stop(self):
        if self.is_running():
            self.captive_portal.find("enable").decompose()
            self.__apply_config()

    def get_status(self):
    # https://pfrest.org/api-docs/#/STATUS/getStatusSystemEndpoint
        try:
            return self.connection.exec("hostname; uptime; ifconfig").stdout
        except Exception as e:
            return "Error reading state:" + str(e)

    def get_applied_theme_id(self):
        try:
            self.__read_config()
            htmltext = self.captive_portal.find("htmltext").text
            htmltext = BeautifulSoup(
                base64.b64decode(htmltext), features='lxml')
            return htmltext.find("meta", {"name": "theme_id"})['content']
        except:
            return ""

    def apply_theme(self, src):
        try:
            self.__read_config()
            src_files = os.listdir(src)
            for file_name in src_files:
                full_file_name = os.path.join(src, file_name)
                if file_name in ["htmltext.html", "errtext.html", "logouttext.html"]:
                    # reading theme stored on this computer
                    with open(full_file_name, 'r') as file:
                        page = file.read()
                    page = str(base64.b64encode(bytes(page, 'utf-8')), "utf8")
                    print(page)
                    self.captive_portal.find(file_name.replace(
                        ".html", "")).string = page

            self.__apply_config()
        except Exception as e:
            return "Error applying theme: " + str(e)


    def apply_auth(self, auth_protocol, auth_url, auth_timeout, auth_method):
        try:
            self.__read_config()

            self.captive_portal.find("auth_method").string = auth_protocol  #TODO
            self.captive_portal.find("auth_method").string = auth_method
            self.captive_portal.find("auth_server").string = auth_url
            self.captive_portal.find("timeout").string = auth_timeout

            self.__apply_config()

        except Exception as e:
            return "Error applying authentication method: " + str(e)


    def get_logfile_content(self):
        return self.connection.read_file(self.log_filename)
