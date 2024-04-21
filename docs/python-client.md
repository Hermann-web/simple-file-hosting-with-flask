# File Sharing Python Client Documentation

## Overview

This document serves as a developer guide for the File Sharing Python Client, which provides a convenient way to interact with the File Sharing API using Python code. Methods include login, file listing, file uploading, file downloading (different techniques), and logout.

## Installation

You can install the Python client package using pip:

```bash
pip install flask-file-share
```

## Usage

1. **Initialize the Client**

   ```python
   from pathlib import Path
   import flask_file_share as ffs

   username = "your_username"  # replace with your username
   password = "your_password"  # replace with your password
   base_url = "http://localhost:5000"  # replace with your server URL

   client = ffs.Client(username=username, password=password, base_url=base_url)
   ```

2. **Login**

   ```python
   client.login()
   ```

3. **List Files**

   ```python
   client.list_files(nb_files=10, order="desc")
   ```

4. **Upload a File**

   ```python
   file_path = Path("path/to/your/file.txt")
   client.upload_file(file_path)
   ```

5. **Download a File**

   ```python
   filename = "file.txt"  # replace with the filename you want to download
   output_folder = Path("path/to/save")
   client.download_file(filename, output_folder)
   ```

6. **Download Last N Files**

   ```python
   nb_files = 5  # replace with the number of files you want to download
   output_folder = Path("path/to/save")
   client.download_last_n_files(nb_files, output_folder)
   ```

7. **Logout**

   ```python
   client.logout()
   ```

## Notes

- Replace `"your_username"`, `"your_password"`, and `"http://localhost:5000"` with your actual username, password, and server URL respectively.
- Adjust file paths and filenames according to your system.
