"""
settings for the project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file if it exists
dotenv_path = '.env'
if os.path.exists(dotenv_path):
    logging.warning("loading .env file")
    load_dotenv(dotenv_path)
else:
    logging.warning(".env file not found")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

UPLOADS_DATA_DIR = BASE_DIR.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

UPLOAD_FOLDER = Path(os.getenv('UPLOAD_FOLDER', UPLOADS_DATA_DIR / "uploads")).absolute()
UPLOAD_FOLDER.mkdir(exist_ok=True)

DATA_FILE = Path(os.getenv('DATA_FILE', UPLOADS_DATA_DIR / "data.json")).absolute()
assert DATA_FILE.parent.exists()

STATIC_FOLDER = (BASE_DIR / "static").absolute()
assert STATIC_FOLDER.exists() and not STATIC_FOLDER.is_file(), f"STATIC_FOLDER={STATIC_FOLDER} does not exists as a folder"

TEMPLATES_FOLDER = (BASE_DIR / "templates").absolute()
assert TEMPLATES_FOLDER.exists() and not STATIC_FOLDER.is_file()

USERNAME_STR = 'FM_USERNAME'
PASSWORD_STR = 'FM_PASSWORD'
SECRET_KEY_STR = 'FM_SECRET_KEY'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
if 0:
    # Set default values for username, password, and secret key
    if DEBUG:
        USERNAME = os.getenv(USERNAME_STR, 'default_username')
        PASSWORD = os.getenv(PASSWORD_STR, 'default_password')
        SECRET_KEY = os.getenv(SECRET_KEY_STR, 'default_secret_key')
    else:
        # Raise error if DEBUG is False and username, password, or secret key is not provided
        if USERNAME_STR not in os.environ or PASSWORD_STR not in os.environ or SECRET_KEY_STR not in os.environ:
            raise ValueError("You must provide USERNAME, PASSWORD, and SECRET_KEY in production mode (DEBUG=False).")

        USERNAME = os.environ[USERNAME_STR]
        PASSWORD = os.environ[PASSWORD_STR]
        SECRET_KEY = os.environ[SECRET_KEY_STR]

    logging.warning(f"DEBUG: {DEBUG}")
    logging.warning(f"USERNAME: {USERNAME}")
    logging.warning(f"PASSWORD: {PASSWORD}")
    logging.warning(f"SECRET_KEY: {SECRET_KEY}")


else:
    # Set default values for username, password, and secret key
    if DEBUG:
        USERNAME = os.getenv(USERNAME_STR, 'default_username')
        PASSWORD = os.getenv(PASSWORD_STR, 'default_password')
        SECRET_KEY = os.getenv(SECRET_KEY_STR, 'default_secret_key')
    else:
        USERNAME = os.getenv(USERNAME_STR)
        PASSWORD = os.getenv(PASSWORD_STR)
        SECRET_KEY = os.getenv(SECRET_KEY_STR)

        # Raise error if DEBUG is False and username, password, or secret key is not provided
        if USERNAME is None or PASSWORD is None or SECRET_KEY is None:
            raise ValueError("You must provide USERNAME, PASSWORD, and SECRET_KEY in production mode (DEBUG=False).")


    logging.warning(f"DEBUG: {DEBUG}")
    logging.warning(f"USERNAME: {USERNAME}")
    logging.warning(f"PASSWORD: {PASSWORD}")
    logging.warning(f"SECRET_KEY: {SECRET_KEY}")
