"""Import necessary libraries and modules."""
import json
import mimetypes
import os
import sys
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from slugify import slugify

sys.path.append(".")
from src.constants import (
    DATA_FILE,
    DEBUG,
    FLASK_SECRET_KEY,
    PASSWORD,
    STATIC_FOLDER,
    UPLOAD_FOLDER,
    USERNAME,
)
from src.utils import create_zip_archive

app = Flask(__name__, static_folder=str(STATIC_FOLDER))

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DATA_FILE"] = DATA_FILE
app.config["SECRET_KEY"] = FLASK_SECRET_KEY
app.config["DEBUG"] = DEBUG
app.config["USERNAME"] = USERNAME
app.config["PASSWORD"] = PASSWORD

# Set the session timeout to 30 minutes (1800 seconds)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)


def validate_credentials(username, password):
    """
    Validate user credentials.

    Args:
        username (str): Username provided by the user.
        password (str): Password provided by the user.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    res = username == app.config["USERNAME"] and password == app.config["PASSWORD"]
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


@app.route("/")
@login_required
def index():
    """Render the index page."""
    files = get_files_with_dates()
    return render_template("index.html", files=files)


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
            jsonify(
                {
                    "message": 'Invalid value for parameter "order". Must be "asc" or "desc".'
                }
            ),
            400,
        )

    files = get_files_with_dates()
    files = files[-min(nb_files, len(files)) :]

    # Sort files based on the specified order
    if order == "asc":
        files = sorted(files, key=lambda x: x[1])
    else:
        files = sorted(files, key=lambda x: x[1], reverse=True)

    return jsonify({"files": files})


def get_files_with_dates():
    """Retrieve files with their modification dates."""
    data = load_data_from_json()
    return [
        (filename, data[filename])
        for filename in sorted(data, key=data.get)
        if (app.config["UPLOAD_FOLDER"] / filename).exists()
    ]


def load_data_from_json():
    """
    Load data from JSON file.

    Returns:
        dict: Loaded data from the JSON file.
    """
    if os.path.exists(app.config["DATA_FILE"]):
        with open(app.config["DATA_FILE"], "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                pass
    return {}


def sucessful_login_redirect():
    """Redirect user after successful login."""
    return redirect(session.pop("previous_url") if "previous_url" in session else "\\")


def default_login_render():
    """Render default login page."""
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if is_logged_in():
        return sucessful_login_redirect()

    if request.method != "POST":
        return default_login_render()

    username = request.form["username"]
    password = request.form["password"]

    if validate_credentials(username, password):
        return sucessful_login_redirect()

    return default_login_render()


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
    session.clear()
    return redirect("/login")


@app.route("/api/logout")
def api_logout():
    """Handle API user logout."""
    session.clear()
    return jsonify({"message": "Logged out"})


def handle_file_saving(file):
    """Handle saving of uploaded files."""
    filename = slugify_filename(file.filename)
    file_save = app.config["UPLOAD_FOLDER"] / filename
    print(f"saving {file_save.resolve()}")
    file.save(file_save)
    update_data_file(filename)
    return filename


def slugify_filename(filename):
    """
    Slugify filename.

    Args:
        filename (str): Original filename.

    Returns:
        str: Slugified filename.
    """
    # Split the filename and extension
    _ = filename.rsplit(".", 1)
    assert len(_) == 2
    base, extension = _
    # Slugify the base part
    slug_base = slugify(base)
    # Join the slugified base with the original extension
    slug_filename = f"{slug_base}.{extension}"
    return slug_filename


@app.route("/upload", methods=["POST"])
@login_required
def upload():
    """Handle file upload."""
    file = request.files["file"]
    if file:
        handle_file_saving(file)
    return redirect("/")


@app.route("/api/upload", methods=["POST"])
@api_login_required
def api_upload():
    """Handle API file upload."""
    file = request.files["file"]
    if not file:
        return jsonify({"message": "No file provided"}), 400
    filename = handle_file_saving(file)
    return jsonify({"message": f"File uploaded: {filename}"})


def update_data_file(filename):
    """Update data file with new file information."""
    data = load_data_from_json()
    data[filename] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(app.config["DATA_FILE"], "w", encoding="utf-8") as file:
        json.dump(data, file)


@app.route("/uploads/<path:filename>")
@login_required
def download(filename):
    """Handle file download."""

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/api/uploads/<path:filename>")
@api_login_required
def api_download(filename):
    """Handle API file download."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# Function to get the last n files
def get_last_n_files(nb_files):
    """Get the last n files."""
    data = load_data_from_json()
    files = sorted(data, key=data.get, reverse=True)[:nb_files]
    return files


@app.route("/api/last/<int:nb_files>/download")
@api_login_required
def api_last_n_files_download(nb_files):
    """Handle API download of last n files."""
    files = get_last_n_files(nb_files)

    # Get the filename from the query parameters or generate a unique filename
    filename = request.args.get("filename", None)

    # Call the create_zip_archive function from utils.py with the specified or generated filename
    filename, zip_data = create_zip_archive(
        files, app.config["UPLOAD_FOLDER"], filename=filename
    )

    # Prepare response with ZIP archive
    response = make_response(zip_data)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "application/zip"

    return response


def get_content_type(file_path):
    """
    Get content type based on file extension.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Content type of the file.
    """
    # Determine the content type based on the file extension
    mime_type, _ = mimetypes.guess_type(file_path)

    # Map .md and .mmd extensions to text/plain
    if mime_type in ("text/markdown", "text/x-markdown"):
        mime_type = "text/plain"
    if file_path.endswith(".md") or file_path.endswith(".mmd"):
        mime_type = "text/plain"

    return mime_type


@app.route("/open/<path:filename>")
@login_required
def open_file(filename):
    """Open a file."""
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return "File not found"

    mime_type = get_content_type(file_path)

    # Map .md and .mmd extensions to text/plain
    if mime_type in ("text/markdown", "text/x-markdown"):
        mime_type = "text/plain"

    if mime_type:
        with open(file_path, "rb") as file:
            file_content = file.read()
        return Response(file_content, content_type=mime_type)

    return "Unknown file type"


@app.route("/raw/<path:filename>")
@login_required
def raw_file(filename):
    """Return raw file content."""
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return "File not found"

    with open(file_path, "rb") as file:
        file_content = file.read()
    return file_content


# Serve static files from the 'static' folder
@app.route("/<path:filename>")
def static_files(filename):
    """Serve static files."""
    return send_from_directory(STATIC_FOLDER, filename)


@app.after_request
def add_header(response):
    """
    Add headers to tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


if __name__ == "__main__":
    app.run()
