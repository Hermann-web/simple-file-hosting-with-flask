import argparse
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from cli_app.cli_app import FileSharingClient

DEFAULT_BASE_URL = "http://localhost:5000"

@contextmanager
def cli_app_session_manager(host, username, password) -> Generator[FileSharingClient, None, None]:
    cli_app = FileSharingClient(username=username, password=password, base_url= host)
    # create a session
    cli_app.login()
    try:
        yield cli_app
    finally:
        # logout even if exception occurs in the block
        cli_app.logout()

def main():
    parser = argparse.ArgumentParser(description='File sharing CLI')
    parser.add_argument('command', choices=['login', 'logout', 'list', 'upload', 'download', 'downloadl'], help='Command to execute')
    parser.add_argument('--host', help=f'host server: default={DEFAULT_BASE_URL}', default=DEFAULT_BASE_URL)
    parser.add_argument('--username', help='Username')
    parser.add_argument('--password', help='Password')
    parser.add_argument('--file', help='File to upload or download')
    parser.add_argument('--output', help='Directory or file path to save the downloaded file')
    parser.add_argument('--n', type=int, help='Number of files to list or download')
    parser.add_argument('--order', choices=['asc', 'desc'], help='Order of files to list or download')
    args = parser.parse_args()

    if not (args.username and args.password):
        print('Please provide a username and password')
        return

    with cli_app_session_manager(host=args.host, username=args.username, password=args.password) as cli_app:
        assert isinstance(cli_app, FileSharingClient)
        print("\n>>>proceed...\n")
    
        
        if args.command in ['login','logout']:
            return
                 
        elif args.command == 'list':
            n = args.n if args.n else 10
            order = args.order if args.order else 'desc'
            cli_app.list_files(n=n, order=order)
        
        elif args.command == 'upload':
            if not args.file:
                print('Please provide a file to upload')
                return
            cli_app.upload_file(args.file)
            
        elif args.command == 'download':
            if not args.file:
                print('Please provide a file to download')
                return
            
            file_to_download = args.file

            folder = Path(args.output) if args.output else Path('fileshared')
            folder.mkdir(exist_ok=True)
            
            if folder.is_dir():
                filename = ''
            elif folder.is_file():
                folder, filename = folder.parent, folder.stem
            else:
                print('Invalid output path')
                return

            cli_app.download_file(file_to_download, folder, save_filename=filename, order=args.order)
        
        elif args.command == 'downloadl':
            if not args.n:
                print('Please provide the number of files to download')
                return
            
            n = args.n

            folder = Path(args.output) if args.output else Path('fileshared')
            folder.mkdir(exist_ok=True)
            
            if folder.is_dir():
                filename = ''
            elif folder.is_file():
                folder, filename = folder.parent, folder.stem
            else:
                print('Invalid output path')
                return

            cli_app.download_last_n_files(n, folder, filename)

if __name__ == '__main__':
    main()
