"""
Filename: themes.py
Author: Bc. Ondřej Mikula @ FIT BUT
Project: Captive Portal Management System
Date: 2024-2025
License: MIT License
Contact: xmikul69@vut.cz
"""

import os
import traceback

from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file, after_this_request
import flask_login


def define_gui(app, application_layer):

    @app.route('/gui/themes', methods=['GET'])
    @app.route('/gui/themes/list', methods=['GET'])
    @flask_login.login_required
    def gui_list_themes_single():
        mode = application_layer.get_settings_mode()
        if mode == "single":
            portal_id = application_layer.get_single_portal_name()
            return gui_list_themes(portal_id)
        elif mode == "pool":
            application_layer.list_themes()
            return gui_list_themes("")

        return "", 404

    @app.route('/gui/themes/list/<portal_id>', methods=['GET'])
    @flask_login.login_required
    def gui_list_themes(portal_id):
        themes_list = application_layer.list_themes()
        return render_template('themes.html', themes_list=themes_list, current_theme_id=application_layer.get_applied_theme_id(portal_id), application_layer=application_layer, portal_id=portal_id)

    @app.route('/gui/themes/apply/<theme_id>', methods=['POST'])
    @flask_login.login_required
    def gui_theme_apply_single(theme_id):
        portal_id = application_layer.get_single_portal_name()
        return gui_theme_apply(theme_id, portal_id)

    @app.route('/gui/themes/apply/<theme_id>/<portal_id>', methods=['POST'])
    @flask_login.login_required
    def gui_theme_apply(theme_id, portal_id):
        src_dir = os.path.join(app.config['THEMES_FOLDER'], theme_id)
        application_layer.apply_theme(portal_id, src_dir)
        return redirect(url_for('gui_list_themes', portal_id=portal_id))

    @app.route('/gui/themes/download/<theme_id>', methods=['GET'])
    @flask_login.login_required
    def gui_download_theme(theme_id):
        try:
            @after_this_request
            def delete_tmpzip(response):
                try:
                    os.remove(zipfile_fname)
                    return response
                except Exception:
                    return response

            zipfile_fname = application_layer.prepare_theme_for_download(theme_id)
            return send_file(zipfile_fname)
        except FileNotFoundError:
            return render_template('errors/error.html', message="Theme Not Found"), 404
        except Exception as e:
            return render_template('errors/error.html', message="Error downloading theme:" + str(e)), 400

    @app.route('/gui/themes/delete/<theme_id>', methods=['POST'])
    @flask_login.login_required
    def gui_delete_theme(theme_id):
        try:
            method = request.form['method']
            portal_id = request.form['portal_id']
            if method == "DELETE":
                application_layer.delete_theme(theme_id)

        except Exception as e:
            return render_template('errors/error.html', message="Error deleting theme:" + str(e)), 400

        return redirect(url_for('gui_list_themes', portal_id=portal_id))

    @app.route('/gui/themes', methods=['POST'])
    @flask_login.login_required
    def gui_upload_theme():
        theme_file = request.files['theme']
        portal_id = request.form['portal_id']
        application_layer.upload_theme(theme_file)

        return redirect(url_for('gui_list_themes', portal_id=portal_id))

    @app.route('/gui/themes/scrape', methods=['POST'])
    @flask_login.login_required
    def gui_scrape_theme():
        splash_url = request.form['splash_url']
        status_url = request.form['status_url']
        theme_id = request.form['id']
        auth_method = request.form['auth_method']
        portal_id = request.form['portal_id']
        application_layer.scrape_theme(splash_url, status_url, theme_id, auth_method)

        return redirect(url_for('gui_list_themes', portal_id=portal_id))

    @app.route('/gui/themes/preview/<theme_id>')
    @flask_login.login_required
    def gui_theme_preview(theme_id):
        try:
            temp_filename = application_layer.get_theme_preview(theme_id)
            return send_file(temp_filename, mimetype='image/jpg')
        except FileNotFoundError:
            return render_template('errors/error.html', message="Image Not Found"), 404
        except Exception as e:
            traceback.print_exc()
            return render_template('errors/error.html', message="Error reading image:" + str(e)), 400
