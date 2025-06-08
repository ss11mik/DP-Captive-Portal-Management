"""
Filename: _connection.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""



def get_from_single_connection(self, key):
    connection_name = self.get_from_single_portal("connection")
    return self.get("connection." + connection_name, key)

def get_from_connection(self, connection_name, key):
    return self.get("connection." + connection_name, key)

def set_for_single_connection(self, key, value):
    connection_name = self.get_from_single_portal("connection")
    self.config.set("connection." + connection_name, key, value)
    self.commit_config()

def set_for_connection(self, connection_name, key, value):
    self.config.set("connection." + connection_name, key, value)
    self.commit_config()

def get_connections(self):
    return [connection.removeprefix("connection.") for connection in self.config.sections() if connection.startswith("connection.")]

def get_single_connection(self):
    return self.get_from_single_portal("connection")

def create_connection(self, connection_id, connection_type):
    self.config.add_section("connection." + connection_id)
    self.set_for_connection(
        connection_id, "connection_type", connection_type)

