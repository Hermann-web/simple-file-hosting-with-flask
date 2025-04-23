"""
File: client.py
---------------

Python client for interacting with the File Sharing Flask application.

Class:
    FileSharingClient: A client class for interacting with the File Sharing Flask application.

Functions:
    main(): Main function to execute CLI commands.

Usage:
    import flask_file_share as ffs

    # Initialize the client
    client = ffs.Client(username="your_username", password="your_password", base_url="http://localhost:5000")

    # Example usage:
    client.login()
    client.upload_file("path/to/your/file.txt")
    client.list_files()
    client.download_file("filename.txt", "path/to/save")
    client.download_last_n_files(5, "path/to/save")
    client.logout()
"""

import json
from pathlib import Path
from typing import Optional, Union

import requests


class FileSharingClient:

    def __init__(self, username: str, password: str, base_url: str):
        """
        Initialize the FileSharingClient instance.

        Parameters
        ----------
        username : str
            The username for authentication.
        password : str
            The password for authentication.
        base_url : str
            The base URL of the server.

        """
        self.username = username
        self.password = password
        print(f"\n>>>base_url ={base_url}")
        self.base_url = f"{base_url}/api"
        self.session = requests.Session()
        self.is_logged_in = False

        self.files: list = []

    def login(self):
        """
        Log in to the server.

        """
        print("\n>>>", end="")
        url = f"{self.base_url}/login"
        headers = {"Content-Type": "application/json"}
        data = json.dumps({"username": self.username, "password": self.password})
        response = self.session.post(url, data=data, headers=headers)
        print(response.text)
        if response.status_code != 200:
            print(f"Login failed: status_code={response.status_code}")

        response_json = json.loads(response.content.decode())  # json.loads(response.text)
        if response_json.get("message") != "Login successful":
            print(f"Login failed: status_code={response.status_code}")

        print("Login successful")
        # print(response_json)
        self.is_logged_in = True

    def list_files(self, nb_files: int = 10, order: str = "desc"):
        """
        List files on the server.

        Parameters
        ----------
        nb_files : int, optional
            Number of files to list.
        order : str, optional
            Order of listing files.

        """
        if not self.is_logged_in:
            self.login()
        print("\n>>>", end="")
        url = f"{self.base_url}?n={nb_files}&order={order}"
        response = self.session.get(url)
        print(response.text)

        if not response.status_code == 200:
            print(f"Failed to retrieve files: status_code={response.status_code}")
            return

        files: list[tuple[str, str]] = response.json().get("files")
        if not files:
            print(f"No files found: status_code={response.status_code}")
            return

        print("Files:")
        for file in files:
            print(f"date: {file[1]} -> fname: {file[0]}")

        self.files = [elt[0] for elt in files]

    def upload_file(self, file_path: str):
        """
        Upload a file to the server.

        Parameters
        ----------
        file_path : str
            Path to the file to upload.

        """
        if not self.is_logged_in:
            self.login()
        print("\n>>>", end="")
        url = f"{self.base_url}/upload"
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = self.session.post(url, files=files)
            if response.status_code == 200:
                print(f"File uploaded successfully from {file_path}")

            else:
                print(
                    f"Failed to upload file from {file_path} : status_code={response.status_code}")
            print(response.text)

    def download_file(self, filename: str, folder_path: Union[str, Path], save_filename: str = ""):
        """
        Download a file from the server.

        Parameters
        ----------
        filename : str
            Name of the file to download.
        folder_path : Union[str, Path]
            Path to the folder to save the downloaded file.
        save_filename : str, optional
            Name to save the downloaded file as.

        """
        if not self.is_logged_in:
            self.login()
        print("\n>>>", end="")
        url = f"{self.base_url}/uploads/{filename}"
        response = self.session.get(url)

        if response.status_code == 404:
            print(f'file "{filename}" not found : status_code={response.status_code}')
            print(response.text)
            return

        if response.status_code != 200:
            print(f"Failed to download file : status_code={response.status_code}")
            return

        filename = save_filename or filename
        saved_path = Path(folder_path) / filename

        with open(saved_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded and saved to {saved_path.resolve()}")

    def download_last_n_files(self,
                              nb_files: int,
                              folder_path: Union[str, Path],
                              filename: Optional[str] = None):
        """
        Download the last N files from the server.

        Parameters
        ----------
        nb_files : int
            Number of files to download.
        folder_path : Union[str, Path]
            Path to the folder to save the downloaded files.
        filename : str, optional
            Name to save the downloaded file as.

        """
        if not self.is_logged_in:
            self.login()

        url = f"{self.base_url}/last/{nb_files}/download"
        params = {"filename": filename} if filename else None

        response = self.session.get(url, params=params)

        if response.status_code != 200:
            print(f"Failed to download last {nb_files} files: status_code={response.status_code}")
            return

        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            _filename = content_disposition.split("filename=")[1].strip('"')
        else:
            _filename = f"last_{nb_files}_files.zip"

        saved_path = Path(folder_path) / _filename
        with open(saved_path, "wb") as file:
            file.write(response.content)

        print(f"Last {nb_files} files downloaded and saved to {saved_path.resolve()}")

    def logout(self):
        """
        Log out from the server.

        """
        if not self.is_logged_in:
            self.login()
        print("\n>>>", end="")
        url = f"{self.base_url}/logout"
        response = self.session.get(url)
        if response.status_code == 200:
            print("Logout successful")
        else:
            print(f"Logout failed : status_code={response.status_code}")
            print(response.text)


def main():
    """
    Main function to execute CLI commands.

    """
    username = "****"  # put your user token here #the one in the .env file
    password = "****"  # put your user key here #the one in the .env file
    base_url = "http://localhost:5000"
    # Example usage:
    input_folder = Path("tests/data")
    assert input_folder.exists(), f"{input_folder.absolute()} not found"
    output_folder = Path("tests/output")
    output_folder.mkdir(exist_ok=True)
    client = FileSharingClient(username=username, password=password, base_url=base_url)
    client.login()
    client.upload_file(input_folder / "test_file1.txt")
    client.download_file("noexistant_file", output_folder)
    client.list_files()
    client.upload_file(input_folder / "test_file2.txt")
    client.download_file("test_file2.txt", output_folder)
    client.list_files()
    client.download_last_n_files(5, output_folder)
    client.logout()


if __name__ == "__main__":
    main()
