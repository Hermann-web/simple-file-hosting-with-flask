import mimetypes
from typing import Union


def get_file_content_type(file_path: str) -> Union[str, None]:
    """
    Get content type based on file extension using the mimetypes built-in library.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Content type of the file.
    """
    # Determine the content type based on the file extension
    mime_type, _ = mimetypes.guess_type(file_path)

    return mime_type
