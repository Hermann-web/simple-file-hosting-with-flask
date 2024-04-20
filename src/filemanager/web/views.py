from typing import List

from flask import render_template


def render_login_page():
    """Render default login page."""
    return render_template("login.html")


def render_index_page(files: List):
    """Render index page."""
    return render_template("index.html", files=files)
