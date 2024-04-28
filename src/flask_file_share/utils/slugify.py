"""
File: slugify.py
----------------

A utility module for slugifying filenames.
"""

from pathlib import Path
from typing import Union
from slugify import slugify  # pylint: disable=E0401


def slugify_filepath(filename: Union[str, Path]) -> Path:
    """
    Slugify the filename.

    Parameters
    ----------
    filename : str
        The original filename.

    Returns
    -------
    str
        The slugified filename.
    """
    filename = Path(filename)
    # Slugify the base part
    slug_base = slugify(filename.stem)
    extension = filename.suffix.lower()
    # Join the slugified base with the original extension
    slug_filename = f"{slug_base}{extension}"
    return filename.parent / slug_filename

def slugify_filename(filename: Union[str, Path]) -> str:
    return str(slugify_filepath(filename))
