"""
File: utils.py
--------------

Utility functions for the File Sharing Flask application.

Functions:

    - load_data_from_json(): Load data from the JSON file.
    - get_files_with_dates(): Retrieve files with their modification dates.
    - update_data_file(filename: str): Update the data file with new file information.
    - handle_file_saving(file: FileStorage) -> str: Handle saving of uploaded files.
    - get_last_n_files(nb_files: int) -> List[str]: Get the last n files.
    - get_content_type(file_path: str) -> Union[str, None]: Get content type based on file extension.
    - create_sharefile_zip_archive(filepaths: List[str], output_fname: Optional[str] = None) -> Tuple[str, bytes]: Create a ZIP archive containing specified files.

Usage:
    These utility functions are used across the application to perform various tasks such as loading data,
    handling file uploads, retrieving file information, and creating ZIP archives.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from werkzeug.datastructures import FileStorage

from .. import settings as st
from ..utils import create_zip_archive, get_file_content_type, slugify_filename


def load_data_from_json() -> Dict[str, str]:
    """
    Load data from the JSON file.

    Returns:
        dict: Loaded data from the JSON file.
    """
    if not st.DATA_FILE.exists():
        return {}

    with open(str(st.DATA_FILE), "r", encoding="utf-8") as file:
        try:
            content = json.load(file)
        except json.JSONDecodeError:
            content = {}

    assert isinstance(content, dict)
    return content


def get_files_with_dates() -> List[Tuple]:
    """
    Retrieve files with their modification dates.

    Returns:
        list: List of tuples containing filename and modification dates.
    """
    data = load_data_from_json()
    return [(filename, data[filename])
            for filename in sorted(data, key=data.__getitem__)
            if (st.UPLOAD_FOLDER / filename).exists()]


def update_data_file(filename: str):
    """
    Update the data file with new file information.

    Args:
        filename (str): Name of the file to update.
    """
    data = load_data_from_json()
    data[filename] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(str(st.DATA_FILE), "w", encoding="utf-8") as file:
        json.dump(data, file)


def handle_file_saving(file: FileStorage) -> str:
    """
    Handle saving of uploaded files.

    Args:
        file (FileStorage): The uploaded file.

    Returns:
        str: Filename of the saved file.
    """
    filename = file.filename or "file-" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".file"
    filename = slugify_filename(filename)
    file_save = st.UPLOAD_FOLDER / filename
    print(f"saving {file_save.resolve()}")
    file.save(file_save)
    update_data_file(filename)
    return filename


# Function to get the last n files
def get_last_n_files(nb_files: int) -> List[str]:
    """
    Get the last n files.

    Args:
        nb_files (int): Number of files to retrieve.

    Returns:
        list: List of filenames.
    """
    data = load_data_from_json()
    files = sorted(data, key=data.__getitem__, reverse=True)[:nb_files]
    return files


def get_content_type(file_path: str) -> Union[str, None]:
    """
    Get content type based on file extension.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Content type of the file.
    """
    # Determine the content type based on the file extension
    mime_type = get_file_content_type(file_path)

    # Map .md and .mmd extensions to text/plain
    if mime_type in ("text/markdown", "text/x-markdown"):
        mime_type = "text/plain"
    if file_path.endswith(".md") or file_path.endswith(".mmd"):
        mime_type = "text/plain"

    return mime_type


def create_sharefile_zip_archive(filepaths: List[str],
                                 output_fname: Optional[str] = None) -> Tuple[str, bytes]:
    """
    Create a ZIP archive containing specified files.

    Args:
        filepaths (list): List of files to be included in the ZIP archive.
        output_fname (str, optional): Name of the ZIP archive. If not provided,
        a unique filename will be generated.

    Returns:
        tuple: A tuple containing the filename of the ZIP archive and its content as bytes.
    """

    # Generate a unique filename if not provided
    if output_fname is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_fname = f"sharefile_archive_{timestamp}.zip"

    return create_zip_archive(filepaths=filepaths, output_fname=output_fname)
