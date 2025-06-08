# Filename: Makefile
# Author: Bc. Ondřej Mikula @ FIT BUT
# Project: Captive Portal Management System
# Date: 2024-2025
# License: MIT License
# Contact: xmikul69@vut.cz


run:
	source .venv/bin/activate && flask --app CPM run

run_https:
	source .venv/bin/activate && flask --app CPM run --cert=instance/cert.pem --key=instance/key.pem

code_format:
	for f in `find CPM -name "*.py"`; do python -m autopep8 --in-place $f; done

install_service:
	cp captive-portal-management.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable captive-portal-management.service
	systemctl start captive-portal-management.service

docker_image:
	docker build -t "captive-portal-management:1.0" .
