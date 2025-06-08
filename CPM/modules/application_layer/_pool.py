"""
Filename: _pool.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import CPM.modules.backend


def add_to_pool(self, portal_id):
    self.config.add_to_pool(portal_id)
    self.refresh_pool()


def remove_from_pool(self, portal_id):
    self.config.remove_from_pool(portal_id)
    self.refresh_pool()


def refresh_pool(self):
    self.portals = CPM.modules.backend.init_backends(self.app, self.config)
    self.reload_from_config()
