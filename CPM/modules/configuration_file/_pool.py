"""
Filename: _pool.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import json


def add_to_pool(self, portal_id):
    current = self.get_selected_portals()
    current += [portal_id]
    self.set("mode.pool", "portals", json.dumps(current))

def remove_from_pool(self, portal_id):
    current = self.get_selected_portals()
    current.remove(portal_id)
    self.set("mode.pool", "portals", json.dumps(current))
