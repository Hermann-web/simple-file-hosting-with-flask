"""
File: zip.py
------------

A utility module for creating ZIP archives.
"""

import os
import zipfile
from io import BytesIO
from typing import List, Tuple


def create_zip_archive(filepaths: List[str], output_fname: str) -> Tuple[str, bytes]:
    """
    Create a ZIP archive containing specified files.

    Parameters
    ----------
    filepaths : list of str
        List of files to be included in the ZIP archive.
    output_fname : str
        Name of the ZIP archive.

    Returns
    -------
    tuple
        A tuple containing the filename of the ZIP archive and its content as bytes.
    """

    # Create an in-memory ZIP archive
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_path in filepaths:
            zip_file.write(str(file_path), os.path.basename(file_path))

    return output_fname, zip_buffer.getvalue()
