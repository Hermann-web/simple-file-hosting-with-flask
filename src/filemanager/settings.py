"""
settings for the project.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
dotenv_path = ".env"
if os.path.exists(dotenv_path):
    logging.warning("loading .env file")
    load_dotenv(dotenv_path)
else:
    logging.warning(".env file not found")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

UPLOADS_DATA_DIR = BASE_DIR.parent / "uploads"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

UPLOAD_FOLDER = Path(os.getenv("UPLOAD_FOLDER", UPLOADS_DATA_DIR / "files")).resolve()
UPLOAD_FOLDER.mkdir(exist_ok=True)

DATA_FILE = Path(os.getenv("DATA_FILE", UPLOADS_DATA_DIR / "data.json")).resolve()
assert DATA_FILE.parent.exists()

STATIC_FOLDER = (BASE_DIR / "static").resolve()
if not STATIC_FOLDER.exists() or STATIC_FOLDER.is_file():
    raise NotADirectoryError(f"STATIC_FOLDER={STATIC_FOLDER} does not exists as a folder")

TEMPLATES_FOLDER = (BASE_DIR / "templates").resolve()
if not TEMPLATES_FOLDER.exists() or TEMPLATES_FOLDER.is_file():
    raise NotADirectoryError(f"TEMPLATES_FOLDER={TEMPLATES_FOLDER} does not exists as a folder")

USERNAME_STR = "FM_USERNAME"
PASSWORD_STR = "FM_PASSWORD"
SECRET_KEY_STR = "FM_SECRET_KEY"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Set values for username, password, and secret key
if not DEBUG:
    _cdt1 = USERNAME_STR in os.environ
    _cdt2 = PASSWORD_STR in os.environ
    _cdt3 = SECRET_KEY_STR in os.environ
    # Raise error if DEBUG is False and username, password, or secret key is not provided
    if not _cdt1 or not _cdt2 or not _cdt3:
        raise ValueError(
            "You must provide USERNAME, PASSWORD, and SECRET_KEY in production mode (DEBUG=False).")

    USERNAME = os.environ[USERNAME_STR]
    PASSWORD = os.environ[PASSWORD_STR]
    SECRET_KEY = os.environ[SECRET_KEY_STR]

if DEBUG:
    USERNAME = os.getenv(USERNAME_STR, "default_username")
    PASSWORD = os.getenv(PASSWORD_STR, "default_password")
    SECRET_KEY = os.getenv(SECRET_KEY_STR, "default_secret_key")

    logging.warning(f"DEBUG: {DEBUG}")
    logging.warning(f"USERNAME: {USERNAME}")
    logging.warning(f"PASSWORD: {PASSWORD}")
    logging.warning(f"SECRET_KEY: {SECRET_KEY}")
