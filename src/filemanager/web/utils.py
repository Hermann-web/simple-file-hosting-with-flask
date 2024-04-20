import mimetypes
from .. import settings as st
import json 
from datetime import datetime
from slugify import slugify

from werkzeug.datastructures import FileStorage

def load_data_from_json():
    """
    Load data from JSON file.

    Returns:
        dict: Loaded data from the JSON file.
    """
    if st.DATA_FILE.exists():
        with open(str(st.DATA_FILE), "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                pass
    return {}

def get_files_with_dates():
    """Retrieve files with their modification dates."""
    data = load_data_from_json()
    return [
        (filename, data[filename])
        for filename in sorted(data, key=data.get)
        if (st.UPLOAD_FOLDER / filename).exists()
    ]


def update_data_file(filename:str):
    """Update data file with new file information."""
    data = load_data_from_json()
    data[filename] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(str(st.DATA_FILE), "w", encoding="utf-8") as file:
        json.dump(data, file)




def slugify_filename(filename:str):
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

def handle_file_saving(file:FileStorage):
    """Handle saving of uploaded files."""
    filename = slugify_filename(file.filename)
    file_save = st.UPLOAD_FOLDER / filename
    print(f"saving {file_save.resolve()}")
    file.save(file_save)
    update_data_file(filename)
    return filename

# Function to get the last n files
def get_last_n_files(nb_files):
    """Get the last n files."""
    data = load_data_from_json()
    files = sorted(data, key=data.get, reverse=True)[:nb_files]
    return files

def get_content_type(file_path:str):
    """
    Get content type based on file extension.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Content type of the file.
    """
    # Determine the content type based on the file extension
    mime_type, _ = mimetypes.guess_type(file_path)

    # Map .md and .mmd extensions to text/plain
    if mime_type in ("text/markdown", "text/x-markdown"):
        mime_type = "text/plain"
    if file_path.endswith(".md") or file_path.endswith(".mmd"):
        mime_type = "text/plain"

    return mime_type
