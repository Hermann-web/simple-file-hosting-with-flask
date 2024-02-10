import os
from pathlib import Path
from dotenv import load_dotenv

UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

DATA_FILE = Path('data.json')

DEBUG = True  # Set this to True in development environment

# Load environment variables from .env file
load_dotenv()

if not DEBUG:
    USERNAME = os.getenv("S_USERNAME")
    PASSWORD = os.getenv("S_PASSWORD")
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
else:
    USERNAME = "my-username"
    PASSWORD = "my-password"
    FLASK_SECRET_KEY = 'my-secret-key'



assert USERNAME
assert PASSWORD
assert FLASK_SECRET_KEY