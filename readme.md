# File Sharing App

__A simple Flask application for sharing files.__

This Flask-based file manager provides a user-friendly interface for managing files uploaded to the server. It allows users to upload, download, and view files through a web interface. Additionally, it provides an API and a CLI App for programmatic access to file management functionalities.

## Features

### User Authentication

- Users can log in with a username and password to access the file manager's functionalities.
- Authentication is implemented both for web interface access and API access.

### File Management

- Users can upload files to the server through the web interface or API.
- Uploaded files are stored in a specified upload folder on the server.
- File download and viewing functionalities are available through both the web interface and API.

### File Listing and Sorting

- The application provides a list of uploaded files along with their modification dates.
- Users can view the list of files sorted in ascending or descending order by modification date.

### Last N Files Download API

- An API endpoint allows users to download the last N uploaded files as a zip archive.
- Users can specify the number of files to include in the archive and provide a custom filename.

### Markdown File Support

- The application supports viewing Markdown (.md) files directly through the web interface.
- Markdown files are rendered as plain text for easier readability.

<!-- ### PWA Offline Access

- Once installed as a PWA, users can access the application offline, enhancing usability in low-connectivity environments. -->

### Caching Headers

- The application sets caching headers to instruct the browser not to cache the rendered pages, ensuring that users always access the latest content.

### Progressive Web App (PWA) Setup

- The application is configured as a Progressive Web App (PWA), allowing users to install it on their devices and use it like a native app.
- The PWA setup enables offline access, push notifications, and improved performance.

## Installation and Setup

### Prerequisites

- Python 3.x
- Flask
- Python packages specified in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hermann-web/simple-file-hosting-with-flask.git
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask development server:

   ```bash
   python src/app.py
   ```

5. Access the application by visiting [http://localhost:5000](http://localhost:5000) in your web browser.

## Usage

### access the flask web

- The main page displays a list of shared files.
- To upload a file, click on "Upload a File" and select the file you want to share.
- The uploaded files will be listed on the main page for download.

### access the app through an api

- you can access the api with the routes `http://localhost:5000/api/*`
- The file [cli_app/file_sharing_client](/cli_app/file_sharing_client.py) to access the api along with a context manager to handle sessions
- you can read the [api documentation](/docs/api.md)

### access the app's api with a cli app

- The file [cli_app/sharefile.py](/cli_app/sharefile.py) provide a cli app to access the api context manager
- Using your cli, you can get list, upload and download files. The api will be called behind the hood by [cli_app/file_sharing_client](/cli_app/file_sharing_client.py)
- you can read the [api documentation](/cli_app/docs/cli-app.md)

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

2. - __Inspiration from Other Repositories__: The [simple_http_server](https://github.com/freelamb/simple_http_server) repository as an interesting resource for download handlers.

3. __CLI App Enhancement__: Investigate the possibility of implementing bash completion for the CLI app to streamline command-line interactions. Refer to resources and discussions on implementing bash completion for Python applications, such as those found [here](https://stackoverflow.com/questions/8387924/python-argparse-and-bash-completion), to improve usability and efficiency.

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
