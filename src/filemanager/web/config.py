"""Import necessary libraries and modules."""
from datetime import timedelta

from flask import Flask

from .. import settings as st

app = Flask(__name__, static_folder=str(st.STATIC_FOLDER), template_folder=st.TEMPLATES_FOLDER)

app.config["UPLOAD_FOLDER"] = st.UPLOAD_FOLDER
app.config["SECRET_KEY"] = st.SECRET_KEY
app.config["DEBUG"] = st.DEBUG

# Set the session timeout to 30 minutes (1800 seconds)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

__all__ = ["app"]
