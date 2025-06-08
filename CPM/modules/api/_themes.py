"""
Filename: _themes.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import os
import traceback

import flask_login
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request

def define_api_endpoints(app, application_layer):

    @app.route('/api/themes', methods=['GET'])
    @flask_login.login_required
    def api_list_themes():
        """List available themes
        ---
        responses:
          200:
            description: Array of theme IDs
          401:
            description: Unauthorized
        """
        return application_layer.list_themes()

    @app.route('/api/themes/current/<portal_id>', methods=['GET'])
    @flask_login.login_required
    def api_get_current_theme(portal_id):
        """Get currently applied theme of a captive portal
           May be slow or time out, includes connecting to the captive portal.
        ---
        parameters:
          - name: portal_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: ID of current theme
          401:
            description: Unauthorized
        """
        return application_layer.get_applied_theme_id(portal_id)

    @app.route('/api/themes', methods=['PUT'])
    @flask_login.login_required
    def api_upload_theme():
        """Upload a new theme
        ---
        parameters:
          - name: theme
            in: form
            type: file
            required: true
        responses:
          200:
            description: Success
          401:
            description: Unauthorized
        """

        # check if the post request has the file part
        if 'theme' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        theme_file = request.files['theme']
        application_layer.upolad_theme(theme_file)

        return "", 200

    @app.route('/api/themes/scrape', methods=['POST'])
    @flask_login.login_required
    def api_scrape_theme():
        """Create a new theme by scraping
        ---
        parameters:
          - name: url
            in: form
            type: string
            required: true
        responses:
          200:
            description: New theme scraped and added
          400:
            description: invalid URL
          401:
            description: Unauthorized
        """
        theme_url = request.form['url']
        theme_id = request.form['id']
        application_layer.scrape_theme(theme_url, theme_id)

        return "", 200

    @app.route('/api/themes/list/<theme_id>', methods=['GET'])
    @flask_login.login_required
    def api_download_theme(theme_id):
        """Download a theme
        ---
        parameters:
          - name: theme_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: ZIP file with theme files
          401:
            description: Unauthorized
          404:
            description: theme not found
        """
        try:
            @after_this_request
            def delete_tmpzip(response):
                try:
                    os.remove(zipfile_fname)
                    return response
                except Exception:
                    return response
                    # return render_template('error.html', message="Error downloading theme:" + str(e))

            zipfile_fname = application_layer.prepare_theme_for_download(theme_id)
            return send_file(zipfile_fname)
        except FileNotFoundError:
            return "Theme Not Found", 404
        except Exception as e:
            return "Error downloading theme:" + str(e), 400

    @app.route('/api/themes/list/<theme_id>', methods=['DELETE'])
    @flask_login.login_required
    def api_delete_theme(theme_id):
        """Delete a theme
        ---
        parameters:
          - name: theme_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Success
          401:
            description: Unauthorized
        """
        try:
            application_layer.delete_theme(theme_id)

        except Exception as e:
            return ("Error deleting theme:" + str(e)), 400

        return "", 200

    @app.route('/api/themes/list/<theme_id>/apply/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def api_theme_apply(theme_id, portal_id):
        """Apply a theme
           May be slow or time out, includes connecting to the captive portal.
        ---
        parameters:
          - name: theme_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Theme successfully applied
          401:
            description: Unauthorized
          404:
            description: Portal not found
        """
        src_dir = os.path.join(app.config['THEMES_FOLDER'], theme_id)
        application_layer.apply_theme(src_dir, portal_id)
        return "", 200

    @app.route('/api/themes/apply/<theme_id>', methods=['POST'])
    @flask_login.login_required
    def api_theme_apply_single(theme_id):
        """Apply a theme to captive portal in single mode
           May be slow or time out, includes connecting to the captive portal.
        ---
        parameters:
          - name: theme_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Theme successfully applied
          401:
            description: Unauthorized
        """
        portal_id = application_layer.get_single_portal_name()
        src_dir = os.path.join(app.config['THEMES_FOLDER'], theme_id)
        application_layer.apply_theme(src_dir, portal_id)
        return "", 200

    @app.route('/api/themes/list/<theme_id>/preview')
    @flask_login.login_required
    def api_theme_preview(theme_id):
        """Get a preview image of theme
        ---
        parameters:
          - name: theme_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Image of the theme
          401:
            description: Unauthorized
          404:
            description: Image not found
        """
        try:
            temp_filename = application_layer.get_theme_preview(theme_id)
            return send_file(temp_filename, mimetype='image/jpg')
        except FileNotFoundError:
            return "Image Not Found", 404
        except Exception as e:
            traceback.print_exc()
            return "Error reading image:" + str(e), 400
