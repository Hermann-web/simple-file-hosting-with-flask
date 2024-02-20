"""utility function"""
import os
import zipfile
from datetime import datetime
from io import BytesIO


def create_zip_archive(files, upload_folder, filename=None):
    """
    Create a ZIP archive containing specified files.

    Args:
        files (list): List of filenames to be included in the ZIP archive.
        upload_folder (str): Path to the folder where the files are located.
        filename (str, optional): Name of the ZIP archive. If not provided,
        a unique filename will be generated.

    Returns:
        tuple: A tuple containing the filename of the ZIP archive and its content as bytes.
    """
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
