"""
File: mimetype.py
-------------------

A utility module for handling file-related operations.
"""

import mimetypes
from typing import Union


def get_file_content_type(file_path: str) -> Union[str, None]:
    """
    Get the content type based on the file extension using the mimetypes library.

    Parameters
    ----------
    file_path : str
        Path to the file.

    Returns
    -------
    Union[str, None]
        Content type of the file.
    """
    # Determine the content type based on the file extension
    mime_type, _ = mimetypes.guess_type(file_path)

    return mime_type
