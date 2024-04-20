from slugify import slugify


def slugify_filename(filename: str) -> str:
    """
    Slugify filename.

    Args:
        filename (str): Original filename.

    Returns:
        str: Slugified filename.
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
