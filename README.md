# File Sharing App

__A Flask-based file sharing application with enhanced functionalities.__

This Flask-based file sharing app provides a user-friendly interface for accessing files uploaded to the server. It allows users to upload, download, and view files through a web interface. Additionally, it provides an API and a CLI App for programmatic access to file management functionalities.

## Features

- __User Authentication:__

  - Users can log in with a username and password to access the file manager's functionalities.
  - Authentication is implemented for both web interface and API access.

- __File Management:__

  - Users can upload files through the web interface or API, with uploaded files stored in a specified upload folder on the server.
  - Download and viewing functionalities are available through both the web interface and API.

- __File Listing and Sorting:__

  - The application provides a list of uploaded files along with their modification dates.
  - Users can view the list of files sorted in ascending or descending order by modification date.

- __Last N Files Download API:__

  - An API endpoint allows users to download the last N uploaded files as a zip archive.
  - Users can specify the number of files to include in the archive and provide a custom filename.

- __Markdown File Support:__: Markdown (.md) files can be viewed directly through the web interface, rendered as plain text for easier readability.

- __PWA Offline Access:__

  - The application can be installed as a Progressive Web App (PWA), enabling offline access for users.
  - Users can access the application even in low-connectivity environments.

- __Caching Headers:__: The application sets caching headers to ensure users always access the latest content, preventing browser caching of rendered pages.

- __Enhanced CLI Integration:__: Users can run the server and CLI app using the following commands:
  - `ffs-server` or `ffs server` to start the server.
  - `ffs-cli <cli_command> **kwargs` or `ffs cli <cli_command> **kwargs` to run the CLI app.

- __Python Client Package:__

  - Users can install the Python client package with `pip install flask-file-share`, enabling easy programmatic access to file management functionalities.
  - The package provides a client class for interacting with the API, making it simple to upload, download, and list files.

## Installation and Usage

### Installation

1. Install the package directly from PyPI:

   ```bash
   pip install flask-file-share
   ```

1. Start the Flask development server:

   ```bash
   ffs-server
   ```

1. You can instead clone the repository and install the dependencies:

   ```bash
   # Clone the repository
   git clone https://github.com/hermann-web/simple-file-hosting-with-flask.git
   # Create a virtual environment and activate it
   python3 -m venv env
   source env/bin/activate
   # Install the required dependencies
   pip install -r requirements.txt
   # Start the Flask development server
   python src/flask_file_share/app.py
   ```

1. Access the application by visiting [http://localhost:5000](http://localhost:5000) in your web browser.

### Web Interface Usage

The main page displays a list of shared files.

- To upload a file, click on "Upload a File" and select the file you want to share. The uploaded files will be listed on the main page for download.

- You can rewrite the app's setings using a custom `.env` file in the folder you are running the app from.

- You can acces the interface by running one of the following commands: `ffs server`, `ffs-server`, `python src/flask_file_share/app.py`

### API Usage

You can access the api with the routes `http://localhost:5000/api/*`.

- All available features though the we interface are also available though the api

- You can read the [cli app documentation](./docs/api.md)

### Python Client Usage

You can access the api features through a python script. The module [flask_file_share/client](./src/flask_file_share/client.py) accesses the api using a context manager to handle sessions

Here is a usage example:

   ```python
   import flask_file_share as ffs

   username = "****"  # put your user token here
   password = "****"  # put your user key here
   base_url = "http://localhost:5000"

   # Example usage:
   input_folder = Path("examples/data")
   output_folder = Path("examples/output")
   output_folder.mkdir(exist_ok=True)
   client = ffs.Client(username=username, password=password, base_url=base_url)
   client.login()
   client.upload_file(input_folder / "test_file1.txt")
   client.download_file("noexistant_file", output_folder)
   client.list_files()
   client.upload_file(input_folder / "test_file2.txt")
   client.download_file("test_file2.txt", output_folder)
   client.list_files()
   client.download_last_n_files(5, output_folder)
   client.logout()
   ```

You can read the [python client documentation](./docs/python-client.md)

### CLI Usage

- Run the CLI app using:

   ```bash
   ffs-cli <cli_command> **kwargs
   # or
   ffs cli <cli_command> **kwargs
   # or
   python src/flask_file_share/cli.py
   ```

- The file [flask_file_share/app.py](./src/flask_file_share/cli.py) defines a cli app that uses the python client.

- So, Using your cli, you can also access all features available in the python binding.

- you can read the [cli app documentation](./docs/cli-app.md)

## Deployment Guide

To deploy the File Sharing App, follow these steps:

1. Choose a remote server or cloud provider to host your application. Popular options include AWS, Google Cloud, and Heroku.

2. Set up an instance or virtual machine on your chosen server.

3. Connect to your remote server.

4. Install the required dependencies.

5. Modify the Flask application's configuration to use a production-ready web server.

6. Configure your domain or subdomain to point to the IP address of your remote server.

7. Set up SSL/TLS certificates for secure HTTPS communication.

8. Start the Flask application using the production-ready web server.

9. Verify that your file sharing app is accessible.

10. Monitor the deployed application for errors and performance issues.

Remember to follow best practices for securing your deployed application.

## Todo

1. __Extensions Handling__: Improve MIME Content-type for file opening and raw file parsing. Utilize the extensions map from [github/freelamb/simple_http_server](https://github.com/freelamb/simple_http_server/blob/master/simple_http_server.py#L242) to enhance the versatility of file uploads and downloads.

2. __URL Whitelisting__: Implement URL whitelisting feature to restrict access to specific URLs, enhancing security.

3. __Environment Variable Configuration__: Allow users to set server URLs, domain, and port in the `.env` file for easier configuration management.

4. __CLI Integration with .env File__: Enhance the CLI app to read configuration settings from the `.env` file, providing more flexibility and ease of use.

5. __Server Configuration Override__: Provide an option for users to override server configuration settings from the CLI without relying on the `.env` file.

## Contributors

- Hermann AGOSSOU

## License

This project is licensed under the [MIT License](LICENSE).

## Links

- Repository: <https://github.com/hermann-web/simple-file-hosting-with-flask>
- Issue tracker: <https://github.com/hermann-web/simple-file-hosting-with-flask/issues>
- Inspiration and references:
- [Flask](https://flask.palletsprojects.com/) Web framework for Python.
- [Flask PWA demo](https://github.com/uwi-info3180/flask-pwa)

## Contact

For any inquiries or issues, please contact [this mail address](agossouhermann7@gmail.com).
