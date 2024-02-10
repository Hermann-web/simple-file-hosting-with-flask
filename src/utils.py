import os
import zipfile
from io import BytesIO
from datetime import datetime


def create_zip_archive(files, upload_folder, filename=None):
    file_paths = [os.path.join(upload_folder, filename) for filename in files]

    # Create an in-memory ZIP archive
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path, os.path.basename(file_path))

    # Generate a unique filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sharefile_archive_{timestamp}.zip"

    return filename, zip_buffer.getvalue()
