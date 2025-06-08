"""
Filename: nav.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

from flask_nav3 import Nav
from flask_nav3.elements import *

from dominate import tags
from flask_nav3.renderers import Renderer
from flask_nav3 import register_renderer


class BulmaRenderer(Renderer):
    def visit_Navbar(self, node):
        sub = []
        for item in node.items:
            sub.append(self.visit(item))

        return tags.ul(*sub, _class="menu-list")

    def visit_View(self, node):
        title = tags.a(node.text, href=node.get_url())
        if node.active:
            title.attributes["class"] = "is-active"

        return tags.li(title)

    def visit_Subgroup(self, node):
        title = tags.a(node.title)

        if node.active:
            title.attributes["class"] = "is-active"

        return tags.li(title, tags.ul(
            *[self.visit(item) for item in node.items]))


def init(app, config):

    def left_nav():
        mode = config.get("mode", "mode")
        if mode == "single":
            return Navbar(
                View('', ''),
                View('Captive Portal Status', 'gui_status'),
                Subgroup('Configuration',
                    View('Captive Portal', 'gui_config_portal_single'),
                    View('Themes', 'gui_list_themes_single'),
                    View('Authentication', 'gui_config_auth_single'),
                    View('Manage Users', 'gui_list_users_single'),
                    View('Connection', 'gui_connections_single'),
                ),
                View('Captive Portals', 'gui_pool'),
                View('Authentication Servers', 'gui_auth_servers_list'),
                View('Connections', 'gui_connections'),
                View('API Reference', 'gui_doc'),
                View('Settings', 'gui_settings_general'),
                View('Log out', 'gui_logout'),
            )
        elif mode == "pool":
            return Navbar(
                View('', ''),
                View('Captive Portal Status', 'gui_status'),
                View('Captive Portals', 'gui_pool'),
                View('Authenitcation Servers', 'gui_auth_servers_list'),
                View('Connections', 'gui_connections'),
                View('API Reference', 'gui_doc'),
                View('Settings', 'gui_settings_general'),
                View('Log out', 'gui_logout'),
            )

    nav = Nav()
    nav.register_element('left', left_nav)
    nav.init_app(app)
    register_renderer(app, 'bulma', BulmaRenderer)
