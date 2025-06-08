# Filename: Dockerfile
# Author: Bc. Ondřej Mikula @ FIT BUT
# Project: Captive Portal Management System
# Date: 2024-2025
# License: MIT License
# Contact: xmikul69@vut.cz

FROM python:3.13-slim-bullseye
MAINTAINER xmikul69@vut.cz

WORKDIR /CPM

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY CPM CPM
COPY instance instance
COPY .venv .venv

CMD ["flask", "--app", "CPM", "run"]
