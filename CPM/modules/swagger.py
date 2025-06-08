"""
Filename: swagger.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

from flasgger import Swagger


def init(app):
    swagger_config = {
        "title": "Captive Portal Manager API",
        "version": "1.0.0",
        "headers": [
        ],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }

    swagger = Swagger(app, config=swagger_config)
