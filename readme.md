# File Sharing App

A simple Flask application for sharing files.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/hermann-web/simple-file-hosting-with-flask.git
   ```

2. Create a virtual environment and activate it:
   ```shell
   python3 -m venv env
   source env/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the Flask development server:
   ```
   python app.py
   ```

5. Access the application by visiting [http://localhost:5000](http://localhost:5000) in your web browser.

## Usage
### access the flask web 
- The main page displays a list of shared files.
- To upload a file, click on "Upload a File" and select the file you want to share.
- The uploaded files will be listed on the main page for download.

### access the app through an api 
- you can access the api with the routes `http://localhost:5000/api/*`
-  The file [cli_app/cli_app.py](/cli_app/cli_app.py) to access the api along with a context manager to handle sessions
- you can read the [api documentation](/docs/api.md)

### access the app's api with a cli app
- The file [cli_app/sharefile.py](/cli_app/sharefile.py) provide a cli app to access the api context manager
- Using your cli, you can get list, upload and download files. The api will be called behind the hood by [cli_app/cli_app.py](/cli_app/cli_app.py)
- you can read the [api documentation](/docs/cli-app.md)


# Deployment Guide

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


## License

This project is licensed under the [MIT License](LICENSE).
