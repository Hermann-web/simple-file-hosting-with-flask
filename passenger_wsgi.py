import os
from pathlib import Path
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve() / "src"

sys.path.insert(0, str(BASE_DIR))
os.chdir(str(BASE_DIR))
from filemanager.app import app

application = app
