"""
Filename: _status.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import time
import io

import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

def define_api_endpoints(app, application_layer):

  @app.route('/api/status/<portal_id>', methods=['GET'])
  @flask_login.login_required
  def api_status(portal_id):
      """Get whether a captive portal is running
         May be slow or time out, includes connecting to the captive portal.
      ---
      parameters:
        - name: portal_id
          in: path
          type: string
          required: true
      responses:
        200:
          description: True or False
        401:
          description: Unauthorized
        404:
          description: Portal not found
      """
      return str(application_layer.is_running(portal_id))

  @app.route('/api/status/logs/<portal_id>', methods=['GET'])
  @flask_login.login_required
  def api_get_logfile(portal_id):
      """Get log file of captive portal
         May be slow or time out, includes connecting to the captive portal.
      ---
      parameters:
        - name: portal_id
          in: path
          type: string
          required: true
      responses:
        200:
          description: Contents of the logfile
        401:
          description: Unauthorized
        404:
          description: Portal not found
      """
      return str(application_layer.get_logfile(portal_id))

  @app.route('/api/status/logs/download/<portal_id>', methods=['GET'])
  @flask_login.login_required
  def api_download_logfile(portal_id):
      """Download log file of captive portal as a file
         May be slow or time out, includes connecting to the captive portal.
      ---
      parameters:
        - name: portal_id
          in: path
          type: string
          required: true
      responses:
        200:
          description: The logfile
        401:
          description: Unauthorized
        404:
          description: Portal not found
      """
      mem = io.BytesIO()
      mem.write(bytes(application_layer.get_logfile(portal_id), "utf8"))
      mem.seek(0)

      return send_file(
          mem,
          as_attachment=True,
          download_name='logfile.log',
          mimetype='text/plain'
      )

  @app.route('/api/status/stop/<portal_id>', methods=['POST'])
  @flask_login.login_required
  def api_status_stop(portal_id):
      """Stop currently running portal
         May be slow or time out, includes connecting to the captive portal.
      ---
      parameters:
        - name: portal_id
          in: path
          type: string
          required: true
      responses:
        200:
          description: Success
        401:
          description: Unauthorized
        404:
          description: Portal not found
      """
      application_layer.stop(portal_id)
      return "", 200

  @app.route('/api/status/start/<portal_id>', methods=['POST'])
  @flask_login.login_required
  def api_status_start(portal_id):
      """Start captive portal
         May be slow or time out, includes connecting to the captive portal.
      ---
      parameters:
        - name: portal_id
          in: path
          type: string
          required: true
      responses:
        200:
          description: Success
        401:
          description: Unauthorized
        404:
          description: Portal not found
      """
      application_layer.start(portal_id)
      time.sleep(.5)  # so it displays running after reload.
      return "", 200
