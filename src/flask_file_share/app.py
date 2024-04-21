"""
File: main.py
-------------

Main module for running the File Sharing Flask web application.

Functions:
    main(): Main function to run the web application.

Usage:
    The web application is run by executing the main function in this module.

Example:
    python main.py
"""

from flask_file_share.web import app


def main():
    app.run()


if __name__ == "__main__":
    main()
