# File Sharing CLI Application Developer Documentation

## Overview

This document serves as a developer guide for the File Sharing Command-Line Interface (CLI) application. The CLI application provides functionality to interact with a file sharing server including listing, uploading, and downloading files.

## Updates

### 2024/02/10

- Updated the listing method to include new options for listing files (`--n` and `--order`).
- Added a method option to download the last N files from the server.

## Usage

### 1. List Files

To list files from the file sharing server, use the following command:

```bash
python cli_app/sharefile.py list --username your_username --password your_password [--n number] [--order asc|desc]
```

- `--username`: Your username for authentication.
- `--password`: Your password for authentication.
- `--n`: (Optional) Number of files to display (defaults to 10).
- `--order`: (Optional) Order of listing (`asc` for ascending, `desc` for descending; defaults to descending).

### 2. Upload a File

To upload a file to the file sharing server, use the following command:

```bash
python cli_app/sharefile.py upload --username your_username --password your_password --file path/to/file.txt
```

- `--username`: Your username for authentication.
- `--password`: Your password for authentication.
- `--file`: Path to the file to upload.

### 3. Download a File

To download a file from the file sharing server, use the following command:

```bash
python cli_app/sharefile.py download --username your_username --password your_password --file file.txt --output path/to/save/file.txt
```

- `--username`: Your username for authentication.
- `--password`: Your password for authentication.
- `--file`: Name of the file to download.
- `--output`: Path to save the downloaded file.

### 4. Download Last N Files

To download the last N files from the file sharing server, use the following command:

```bash
python cli_app/sharefile.py downloadl --username your_username --password your_password --n number --output path/to/save
```

- `--username`: Your username for authentication.
- `--password`: Your password for authentication.
- `--n`: Number of files to download.
- `--output`: Path to save the downloaded files.

**Note**: Replace `your_username` and `your_password` with your actual username and password. Adjust the file paths (`path/to/file.txt`, `path/to/save/file.txt`, `path/to/save`) according to your system.
