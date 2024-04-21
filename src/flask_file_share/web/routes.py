"""
File: routes.py
---------------

Route definitions for the File Sharing Flask application.

Functions:
    - index(): Render the index page.
    - api_index(): API endpoint to retrieve file information.
    - login(): Handle user login.
    - api_login(): Handle API user login.
    - logout(): Handle user logout.
    - api_logout(): Handle API user logout.
    - upload(): Handle file upload.
    - api_upload(): Handle API file upload.
    - download(filename: str): Handle file download.
    - api_download(filename: str): Handle API file download.
    - api_last_n_files_download(nb_files: int): Handle API download of last n files.
    - open_file(filename: str): Open a file.
    - raw_file(filename: str): Return raw file content.
    - static_files(filename: str): Serve static files.
    - add_header(response: Response): Add headers to HTTP response.

Usage:
    The routes are accessed through HTTP requests to corresponding endpoints.

Example:
    Accessing the endpoint "/" renders the index page.
"""

from pathlib import Path

from flask import (Response, jsonify, make_response, redirect, request, send_from_directory)

from .auth import (api_login_required, clear_session, is_logged_in, login_required,
                   successful_login_redirect, validate_credentials)
from .config import app
from .utils import (create_sharefile_zip_archive, get_content_type, get_files_with_dates,
                    get_last_n_files, handle_file_saving)
from .views import render_index_page, render_login_page

UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
STATIC_FOLDER = app.config["STATIC_FOLDER"]


@app.route("/")
@login_required
def index():
    """
    Render the index page.

    Returns
    -------
    str
        The rendered index page.
    """
    files = get_files_with_dates()
    return render_index_page(files=files)


@app.route("/api")
@api_login_required
def api_index():
    """
    API endpoint to retrieve file information.

    Returns
    -------
    str
        JSON response containing file information.
    """
    # Check if 'n' query parameter is provided, default to 10 if not provided or invalid
    nb_files = request.args.get("n", type=int, default=10)
    if nb_files <= 0:
        return jsonify({"message": 'Invalid value for parameter "n"'}), 400

    # Check if 'order' query parameter is provided, default to 'desc' if not provided or invalid
    order = request.args.get("order", type=str, default="desc")
    if order not in ["asc", "desc"]:
        return (
            jsonify({"message": 'Invalid value for parameter "order". Must be "asc" or "desc".'}),
            400,
        )

    files = get_files_with_dates()
    files = files[-min(nb_files, len(files)):]

    # Sort files based on the specified order
    if order == "asc":
        files = sorted(files, key=lambda x: x[1])
    else:
        files = sorted(files, key=lambda x: x[1], reverse=True)

    return jsonify({"files": files})


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.

    Returns
    -------
    str
        Rendered login page or redirect to index page.
    """
    if is_logged_in():
        return successful_login_redirect()

    if request.method != "POST":
        return render_login_page()

    username = request.form["username"]
    password = request.form["password"]

    if validate_credentials(username, password):
        return successful_login_redirect()

    return render_login_page()


@app.route("/api/login", methods=["POST"])
def api_login():
    """
    Handle API user login.

    Returns
    -------
    str
        JSON response indicating login status.
    """
    username = request.json.get("username")
    password = request.json.get("password")

    if validate_credentials(username, password):
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/logout")
def logout():
    """
    Handle user logout.

    Returns
    -------
    redirect
        Redirects to the login page.
    """
    clear_session()
    return redirect("/login")


@app.route("/api/logout")
def api_logout():
    """
    Handle API user logout.

    Returns
    -------
    str
        JSON response indicating logout status.
    """
    clear_session()
    return jsonify({"message": "Logged out"})


@app.route("/upload", methods=["POST"])
@login_required
def upload():
    """
    Handle file upload.

    Returns
    -------
    redirect
        Redirects to the index page.
    """
    file = request.files["file"]
    handle_file_saving(file)
    return redirect("/")


@app.route("/api/upload", methods=["POST"])
@api_login_required
def api_upload():
    """
    Handle API file upload.

    Returns
    -------
    str
        JSON response indicating file upload status.
    """
    file = request.files["file"]
    if not file:
        return jsonify({"message": "No file provided"}), 400
    filename = handle_file_saving(file)
    return jsonify({"message": f"File uploaded: {filename}"})


@app.route("/uploads/<path:filename>")
@login_required
def download(filename: str):
    """
    Handle file download.

    Parameters
    ----------
    filename : str
        Name of the file to download.

    Returns
    -------
    Response
        File download response.
    """

    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/api/uploads/<path:filename>")
@api_login_required
def api_download(filename: str):
    """
    Handle API file download.

    Parameters
    ----------
    filename : str
        Name of the file to download.

    Returns
    -------
    Response
        File download response.
    """
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/api/last/<int:nb_files>/download")
@api_login_required
def api_last_n_files_download(nb_files: int):
    """
    Handle API download of last n files.

    Parameters
    ----------
    nb_files : int
        Number of files to download.

    Returns
    -------
    Response
        ZIP archive containing the requested files.
    """
    files = get_last_n_files(nb_files)

    # Get the filename from the query parameters or generate a unique filename
    filename = request.args.get("filename", None)

    # compress the files
    filepaths = [str(Path(UPLOAD_FOLDER) / fname) for fname in files]
    filename, zip_data = create_sharefile_zip_archive(filepaths, output_fname=filename)

    # Prepare response with ZIP archive
    response = make_response(zip_data)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "application/zip"

    return response


@app.route("/open/<path:filename>")
@login_required
def open_file(filename: str):
    """
    Open a file.

    Parameters
    ----------
    filename : str
        Name of the file to open.

    Returns
    -------
    Response
        File content response.
    """
    file_path = Path(UPLOAD_FOLDER) / filename

    if not file_path.exists():
        return "File not found"

    mime_type = get_content_type(str(file_path))

    # Map .md and .mmd extensions to text/plain
    if mime_type in ("text/markdown", "text/x-markdown"):
        mime_type = "text/plain"

    if not mime_type:
        return "Unknown file type"

    with open(file_path, "rb") as file:
        file_content = file.read()
    return Response(file_content, content_type=mime_type)


@app.route("/raw/<path:filename>")
@login_required
def raw_file(filename: str):
    """
    Return raw file content.

    Parameters
    ----------
    filename : str
        Name of the file.

    Returns
    -------
    bytes
        Raw file content.
    """
    file_path = Path(UPLOAD_FOLDER) / filename

    if not file_path.exists():
        return "File not found"

    with open(str(file_path), "rb") as file:
        file_content = file.read()
    return file_content


# Serve static files from the 'static' folder
@app.route("/<path:filename>")
def static_files(filename: str):
    """
    Serve static files.

    Parameters
    ----------
    filename : str
        Name of the static file.

    Returns
    -------
    Response
        Static file response.
    """
    return send_from_directory(STATIC_FOLDER, filename)


@app.after_request
def add_header(response: Response):
    """
    Add headers to tell the browser not to cache the rendered page.

    Note
    ----------
    If we wanted to we could change max-age to 600 seconds which
    would be 10 minutes.

    Parameters
    ----------
    response : Response
        HTTP response.

    Returns
    -------
    Response
        HTTP response with added headers.
    """
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


if __name__ == "__main__":
    app.run()
