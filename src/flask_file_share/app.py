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

import argparse

from flask_file_share.web import app


def build_web_app_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Build Web App parser.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        The ArgumentParser object.

    Returns
    -------
    argparse.ArgumentParser
        The modified ArgumentParser object.

    """
    # parser.add_argument("-u", "--username", help="Username")
    # parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-H",
                        "--host",
                        default="127.0.0.1",
                        help="Hostname/IP the app should listen on. Default is 127.0.0.1.")
    parser.add_argument("-P",
                        "--port",
                        type=int,
                        default=5000,
                        help="Port the app should listen on. Default is 5000.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    return parser


def parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments.

    Returns
    -------
    argparse.Namespace
        The parsed command-line arguments.

    """
    parser = argparse.ArgumentParser(description="File sharing Flask web application")
    parser = build_web_app_parser(parser)
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace):
    app.run(host=args.host, port=args.port, debug=args.debug)
    # app.run()


if __name__ == "__main__":
    parsed_args = parse_args()
    main(args=parsed_args)
