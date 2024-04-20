from functools import wraps

from flask import jsonify, redirect, request, session

from .. import settings as st


def validate_credentials(username, password):
    """
    Validate user credentials.

    Args:
        username (str): Username provided by the user.
        password (str): Password provided by the user.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    res = username == st.USERNAME and password == st.PASSWORD
    session["logged_in"] = res
    return res


def is_logged_in():
    """Check if the user is logged in."""
    return "logged_in" in session and session["logged_in"]


def login_required(func):
    """Decorator to check if user is logged in."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            print("is not logged in")
            session["previous_url"] = request.url
            return redirect("/login")
        return func(*args, **kwargs)

    return decorated_function


def api_login_required(func):
    """Decorator to check if API user is logged in."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return jsonify({"message": "Unauthorized"}), 401
        return func(*args, **kwargs)

    return decorated_function


def sucessful_login_redirect():
    """Redirect user after successful login."""
    return redirect(session.pop("previous_url") if "previous_url" in session else "\\")


def clear_session():
    session.clear()
