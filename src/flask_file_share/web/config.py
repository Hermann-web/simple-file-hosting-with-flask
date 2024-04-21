"""
File: config.py
---------------

Configuration module for the File Sharing Flask application.

Description:
    This module contains configuration settings for the Flask application, including upload folder,
    static folder, and other application-specific configurations.

Usage:
    The configuration settings defined in this module are imported and used throughout the application
    to configure Flask app, such as setting upload folder, static folder, and other Flask app configurations.
"""

from datetime import timedelta

from flask import Flask

from .. import settings as st

app = Flask(__name__, static_folder=str(st.STATIC_FOLDER), template_folder=st.TEMPLATES_FOLDER)

app.config["UPLOAD_FOLDER"] = st.UPLOAD_FOLDER
app.config["STATIC_FOLDER"] = st.STATIC_FOLDER
app.config["SECRET_KEY"] = st.SECRET_KEY
app.config["DEBUG"] = st.DEBUG

# Set the session timeout to 30 minutes (1800 seconds)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=st.PERMANENT_SESSION_LIFETIME_MINUTES)

__all__ = ["app"]
