"""
Filename: __init__.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

from CPM.modules.utils import Utils
from CPM.modules.backend import init_backends
from CPM.modules.configuration_file import CPM_config


class Application_layer:

    def __init__(self, app, portals, auth_servers, config):
        self.portals = portals
        self.auth_servers = auth_servers
        self.app = app
        self.utils = Utils(app)
        self.config = config

    from ._themes import upload_theme, apply_theme, scrape_theme, delete_theme, prepare_theme_for_download, list_themes, get_applied_theme_id, get_theme_preview, get_theme_auth_method
    from ._pool import add_to_pool, remove_from_pool, refresh_pool
    from ._status import get_portal_provider, is_running, get_status, get_logfile, stop, start, get_single_portal_name
    from ._connection import apply_settings_connection, remove_settings_connection, get_single_connection, get_connections, create_connection
    from ._backend import remove_settings_portal, apply_settings_portal, get_portals, get_portals_for_status, create_portal, get_single_portal, get_single_auth_server, get_available_captive_portal_implementations, apply_auth_to_portal
    from ._settings import apply_settings_admin, apply_settings_captive, apply_settings_mode, get_settings_mode
    from ._auth import get_auth_url, get_auth_servers, create_auth_server, auth_server_remove, get_single_auth_server_id, get_auth_server, apply_auth, get_available_auth_server_implementations
    from ._users import get_auth_server_users, get_userfile, restore_users, remove_users_by_id, remove_users_by_username, add_users, add_users_from_file, reset_user_password

    def get_config(self):
        return self.config

    def reload_from_config(self):
        # the main configuration file
        config = CPM_config(self.app.config['CONFIG_FILE'])

        _portals, _auth_servers = init_backends(self.app, config)
        self.portals = _portals
        self.auth_servers = _auth_servers
