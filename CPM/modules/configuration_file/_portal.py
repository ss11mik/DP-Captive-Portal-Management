"""
Filename: _portal.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import json


def get_from_portal(self, portal_name, key):
    return self.get("portal." + portal_name, key)

def set_for_portal(self, portal_name, key, value):
    self.set("portal." + portal_name, key, value)

def get_from_single_portal(self, key):
    portal_name = self.get("mode.single", "portal")
    return self.get("portal." + portal_name, key)

def set_for_single_portal(self, key, value):
    portal_name = self.get("mode.single", "portal")
    self.config.set("portal." + portal_name, key, value)
    self.commit_config()

def create_portal(self, portal_id, implementation, connection, auth_server):
    self.config.add_section("portal." + portal_id)
    self.set_for_portal(portal_id, "implementation", implementation)
    self.set_for_portal(portal_id, "connection", connection)
    self.set_for_portal(portal_id, "auth_server", auth_server)

def remove_portal(self, portal_id):
    self.remove_section(portal_id)
    self.remove_from_pool(portal_id)

def get_portals(self):
    return [portal.removeprefix("portal.") for portal in self.config.sections() if portal.startswith("portal.")]

def get_selected_portals(self):
    return json.loads(self.get("mode.pool", "portals"))

def get_single_portal(self):
    return self.config.get("mode.single", "portal")
