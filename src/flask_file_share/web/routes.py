"""Import necessary libraries and modules."""
from pathlib import Path

from flask import (Response, jsonify, make_response, redirect, request, send_from_directory)

from .auth import (api_login_required, clear_session, is_logged_in, login_required,
                   sucessful_login_redirect, validate_credentials)
from .config import app
from .utils import (create_sharefile_zip_archive, get_content_type, get_files_with_dates,
                    get_last_n_files, handle_file_saving)
from .views import render_index_page, render_login_page

UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
STATIC_FOLDER = app.config["STATIC_FOLDER"]


@app.route("/")
@login_required
def index():
    """Render the index page."""
    files = get_files_with_dates()
    return render_index_page(files=files)


@app.route("/api")
@api_login_required
def api_index():
    """API endpoint to retrieve file information."""
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
    """Handle user login."""
    if is_logged_in():
        return sucessful_login_redirect()

    if request.method != "POST":
        return render_login_page()

    username = request.form["username"]
    password = request.form["password"]

    if validate_credentials(username, password):
        return sucessful_login_redirect()

    return render_login_page()


@app.route("/api/login", methods=["POST"])
def api_login():
    """Handle API user login."""
    username = request.json.get("username")
    password = request.json.get("password")

    if validate_credentials(username, password):
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/logout")
def logout():
    """Handle user logout."""
    clear_session()
    return redirect("/login")


@app.route("/api/logout")
def api_logout():
    """Handle API user logout."""
    clear_session()
    return jsonify({"message": "Logged out"})


@app.route("/upload", methods=["POST"])
@login_required
def upload():
    """Handle file upload."""
    file = request.files["file"]
    if not file.filename:
        return redirect("/")

    handle_file_saving(file)


@app.route("/api/upload", methods=["POST"])
@api_login_required
def api_upload():
    """Handle API file upload."""
    file = request.files["file"]
    if not file:
        return jsonify({"message": "No file provided"}), 400
    filename = handle_file_saving(file)
    return jsonify({"message": f"File uploaded: {filename}"})


@app.route("/uploads/<path:filename>")
@login_required
def download(filename: str):
    """Handle file download."""

    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/api/uploads/<path:filename>")
@api_login_required
def api_download(filename: str):
    """Handle API file download."""
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/api/last/<int:nb_files>/download")
@api_login_required
def api_last_n_files_download(nb_files: int):
    """Handle API download of last n files."""
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
    """Open a file."""
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
    """Return raw file content."""
    file_path = Path(UPLOAD_FOLDER) / filename

    if not file_path.exists():
        return "File not found"

    with open(str(file_path), "rb") as file:
        file_content = file.read()
    return file_content


# Serve static files from the 'static' folder
@app.route("/<path:filename>")
def static_files(filename: str):
    """Serve static files."""
    return send_from_directory(STATIC_FOLDER, filename)


@app.after_request
def add_header(response: Response):
    """
    Add headers to tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


if __name__ == "__main__":
    app.run()
