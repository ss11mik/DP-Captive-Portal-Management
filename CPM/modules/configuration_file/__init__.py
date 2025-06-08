"""
Filename: __init__.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

from configparser import ConfigParser, ExtendedInterpolation


class CPM_config:

    def __init__(self, config_filename):
        self.config_filename = config_filename

        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(config_filename)


    from ._portal import get_from_portal, set_for_portal, get_from_single_portal, set_for_single_portal, create_portal, remove_portal, get_portals, get_selected_portals, get_single_portal
    from ._connection import get_from_single_connection, get_from_connection, set_for_single_connection, set_for_connection, get_connections, get_single_connection, create_connection
    from ._pool import add_to_pool, remove_from_pool
    from ._auth_server import get_auth_servers, create_auth_server, set_for_auth_server, get_from_auth_server, get_single_auth_server_id, get_auth_servers


    def get(self, section, key):
        try:
            return self.config.get(section, key)
        except:
            return ""

    def set(self, section, key, value):
        self.config.set(section, key, value)
        self.commit_config()


    def get_section(self, section):
        return self.config[section]

    def get_from_section(self, key):
        return section.get(key)

    def remove_section(self, section):
        self.config.remove_section(section)
        self.commit_config()

    def commit_config(self):
        with open(self.config_filename, 'w') as configfile:
            self.config.write(configfile)

    def reload_config(self):
        self.config.read(config_filename)






