"""
Filename: _auth_server.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""



def get_auth_servers(self):
    return [auth_server.removeprefix("auth_server.") for auth_server in self.config.sections() if auth_server.startswith("auth_server.")]

def set_for_auth_server(self, auth_server_id, key, value):
    self.config.set("auth_server." + auth_server_id, key, value)
    self.commit_config()

def get_from_auth_server(self, auth_server_id, key):
    return self.get("auth_server." + auth_server_id, key)

def create_auth_server(self, auth_server_id, connection, auth_protocol, auth_url, userfile):
    self.config.add_section("auth_server." + auth_server_id)
    self.set_for_auth_server(auth_server_id, "connection", connection)
    self.set_for_auth_server(auth_server_id, "protocol", auth_protocol)
    self.set_for_auth_server(auth_server_id, "url", auth_url)
    self.set_for_auth_server(auth_server_id, "userfile", userfile)

def get_auth_servers(self):
    return [auth_server.removeprefix("auth_server.") for auth_server in self.config.sections() if auth_server.startswith("auth_server.")]

def get_single_auth_server_id(self):
    return self.get_from_single_portal("auth_server")
