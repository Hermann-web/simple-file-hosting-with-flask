"""
File: slugify.py
----------------

A utility module for slugifying filenames.
"""

from slugify import slugify  # pylint: disable=E0401


def slugify_filename(filename: str) -> str:
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
    # Split the filename and extension
    _ = filename.rsplit(".", 1)
    assert len(_) == 2
    base, extension = _
    # Slugify the base part
    slug_base = slugify(base)
    # Join the slugified base with the original extension
    slug_filename = f"{slug_base}.{extension}"
    return slug_filename
