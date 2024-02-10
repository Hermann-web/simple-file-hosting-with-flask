import argparse
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from file_sharing_client import FileSharingClient

DEFAULT_BASE_URL = "http://localhost:5000"

@contextmanager
def client_session_manager(host, username, password) -> Generator[FileSharingClient, None, None]:
    client = FileSharingClient(username=username, password=password, base_url= host)
    # create a session
    client.login()
    try:
        yield client
    finally:
        # logout even if exception occurs in the block
        client.logout()

def main():
    parser = argparse.ArgumentParser(description='File sharing CLI')
    parser.add_argument('command', choices=['login', 'logout', 'list', 'upload', 'download', 'downloadl'], help='Command to execute')
    parser.add_argument('-H', '--host', help=f'host server: default={DEFAULT_BASE_URL}', default=DEFAULT_BASE_URL)
    parser.add_argument('-u', '--username', help='Username')
    parser.add_argument('-p', '--password', help='Password')
    parser.add_argument('-f', '--file', help='File to upload or download')
    parser.add_argument('-o', '--output', help='Directory or file path to save the downloaded file')
    parser.add_argument('-n', '--nbfiles', type=int, help='Number of files to list or download')
    parser.add_argument('-r', '--order', choices=['asc', 'desc'], help='Order of files to list or download')
    args = parser.parse_args()

    if not (args.username and args.password):
        print('Please provide a username and password')
        return

    with client_session_manager(host=args.host, username=args.username, password=args.password) as file_sharing_client:
        assert isinstance(file_sharing_client, FileSharingClient)
        print("\n>>>proceed...\n")
    
        
        if args.command in ['login','logout']:
            return
                 
        elif args.command == 'list':
            n = args.nbfiles if args.nbfiles else 10
            order = args.order if args.order else 'desc'
            file_sharing_client.list_files(n=n, order=order)
        
        elif args.command == 'upload':
            if not args.file:
                print('Please provide a file to upload')
                return
            file_sharing_client.upload_file(args.file)
            
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

            file_sharing_client.download_file(file_to_download, folder, save_filename=filename, order=args.order)
        
        elif args.command == 'downloadl':
            if not args.nbfiles:
                print('Please provide the number of files to download')
                return
            
            n = args.nbfiles

            folder = Path(args.output) if args.output else Path('fileshared')
            folder.mkdir(exist_ok=True)
            
            if folder.is_dir():
                filename = ''
            elif folder.is_file():
                folder, filename = folder.parent, folder.stem
            else:
                print('Invalid output path')
                return

            file_sharing_client.download_last_n_files(n, folder, filename)

if __name__ == '__main__':
    main()
