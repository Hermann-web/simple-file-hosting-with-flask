"""
File: views.py
--------------

View rendering module for the File Sharing Flask application.

Functions:
    - render_index_page(files: List[Tuple]): Render the index page.
    - render_login_page(): Render the login page.

Usage:
    This module provides functions to render HTML pages for the File Sharing Flask application,
    including the index page and the login page.
"""

from typing import List

from flask import render_template


def render_login_page() -> str:
    """
    Render the default login page.

    Returns
    -------
    str
        The rendered login page.
    """
    return render_template("login.html")


def render_index_page(files: List) -> str:
    """
    Render the index page.

    Parameters
    ----------
    files : List
        List of files to display on the index page.

    Returns
    -------
    str
        The rendered index page.
    """
    return render_template("index.html", files=files)
