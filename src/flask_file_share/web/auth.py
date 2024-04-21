"""
File: auth.py
-------------

Authentication module for the File Sharing Flask application.

Functions:
    - api_login_required(func): Decorator to require API login for a route.
    - clear_session(): Clear user session.
    - is_logged_in(): Check if user is logged in.
    - login_required(func): Decorator to require login for a route.
    - successful_login_redirect(): Redirect user after successful login.
    - validate_credentials(username: str, password: str) -> bool: Validate user credentials.

Usage:
    This module provides authentication-related functionality such as login validation, session management,
    and decorators for requiring login for certain routes.
"""

from functools import wraps

from flask import jsonify, redirect, request, session
from werkzeug.wrappers.response import Response as Wk_Response

from .. import settings as st


def validate_credentials(username: str, password: str) -> bool:
    """
    Validate user credentials.

    Parameters
    ----------
    username : str
        Username provided by the user.
    password : str
        Password provided by the user.

    Returns
    -------
    bool
        True if the credentials are valid, False otherwise.
    """
    res = username == st.USERNAME and password == st.PASSWORD
    session["logged_in"] = res
    return res


def is_logged_in() -> bool:
    """
    Check if the user is logged in.

    Returns
    -------
    bool
        True if the user is logged in, False otherwise.
    """
    return "logged_in" in session and session["logged_in"]


def login_required(func):
    """
    Decorator to check if user is logged in.

    Parameters
    ----------
    func : function
        The function to be decorated.

    Returns
    -------
    function
        Decorated function.
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        """
        Wrapper function to check if the user is logged in before calling the decorated function.

        Returns
        -------
        Any
            Result of the decorated function if the user is logged in, otherwise redirects to login page.
        """
        if not is_logged_in():
            session["previous_url"] = request.url
            return redirect("/login")
        return func(*args, **kwargs)

    return decorated_function


def api_login_required(func):
    """
    Decorator to check if API user is logged in.

    Parameters
    ----------
    func : function
        The function to be decorated.

    Returns
    -------
    function
        Decorated function.
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        """
        Wrapper function to check if the user is logged in before calling the decorated API function.

        Returns
        -------
        Any
            Result of the decorated function if the user is logged in, otherwise returns unauthorized message.
        """
        if not is_logged_in():
            return jsonify({"message": "Unauthorized"}), 401
        return func(*args, **kwargs)

    return decorated_function


def successful_login_redirect() -> Wk_Response:
    """
    Redirect user after successful login.

    Returns
    -------
    Wk_Response
        Flask response for redirecting to the previous URL or the home page.
    """
    return redirect(session.pop("previous_url", "/"))


def clear_session():
    """
    Clear the user session.
    """
    session.clear()
