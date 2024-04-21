"""
File: main.py
------------

CLI module for interacting with the FlaskFileShare application.

Functions:
    create_parser() -> argparse.ArgumentParser:
        Create an ArgumentParser for the CLI.
    main():
        Main function to execute the CLI.

Usage:
    python main.py server
    python main.py cli <cli_command> [-H HOST] [-u USERNAME] [-p PASSWORD] [-f FILE] [-o OUTPUT] [-n NBFILES] [-r ORDER]

Arguments:
    server: Run the web server.
    cli: Run the CLI tool.
    -H, --host: Host server URL. Default is http://localhost:5000.
    -u, --username: Username for authentication.
    -p, --password: Password for authentication.
    -f, --file: File to upload or download.
    -o, --output: Directory or file path to save the downloaded file.
    -n, --nbfiles: Number of files to list or download.
    -r, --order: Order of files to list or download (asc or desc).

Example:
    python main.py server
    python main.py cli list -u myusername -p mypassword -n 5
"""

import argparse

from flask_file_share.app import build_web_app_parser
from flask_file_share.app import main as web_main
from flask_file_share.cli import build_cli_parser
from flask_file_share.cli import main as cli_main


def create_parser() -> argparse.ArgumentParser:
    """
    Create an ArgumentParser for the CLI.

    Returns:
    -------
    argparse.ArgumentParser:
        The ArgumentParser object for the CLI.
    """
    parser = argparse.ArgumentParser(description="FlaskFileShare Application")
    subparsers = parser.add_subparsers(dest="command", help="Select the component to run")

    # Subparser for the web server
    web_app_parser = subparsers.add_parser('server', help='Run the web server')

    # Web-specific arguments
    web_app_parser = build_web_app_parser(web_app_parser)

    # Subparser for the CLI
    cli_parser = subparsers.add_parser('cli', help='Run the CLI tool')

    # CLI-specific arguments
    cli_parser = build_cli_parser(cli_parser)

    return parser


def main():
    """
    Main function to execute the CLI.

    """
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'server':
        web_main(args)
    elif args.command == 'cli':
        # Here, you re-invoke the CLI main with the processed arguments
        cli_main(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
