import argparse

from flask_file_share.app import main as web_main
from flask_file_share.cli import build_cli_parser
from flask_file_share.cli import main as cli_main


def create_parser():
    parser = argparse.ArgumentParser(description="FlaskFileShare Application")
    subparsers = parser.add_subparsers(dest="command", help="Select the component to run")

    # Subparser for the web server
    _ = subparsers.add_parser('server', help='Run the web server')

    # Subparser for the CLI
    cli_parser = subparsers.add_parser('cli', help='Run the CLI tool')

    # CLI-specific arguments
    cli_parser = build_cli_parser(cli_parser)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'server':
        web_main()
    elif args.command == 'cli':
        # Here, you re-invoke the CLI main with the processed arguments
        cli_main(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
