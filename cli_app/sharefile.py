import argparse
from pathlib import Path
from cli_app import cli_app_session_manager

DEFAULT_BASE_URL = "http://localhost:5000"

def main():
    parser = argparse.ArgumentParser(description='File sharing CLI')
    parser.add_argument('command', choices=['login', 'logout', 'list', 'upload', 'download'], help='Command to execute')
    parser.add_argument('--host', help=f'host server: default={DEFAULT_BASE_URL}', default=DEFAULT_BASE_URL)
    parser.add_argument('--username', help='Username')
    parser.add_argument('--password', help='Password')
    parser.add_argument('--file', help='File to upload or download')
    parser.add_argument('--output', help='Directory or file path to save the downloaded file')
    args = parser.parse_args()

    if not (args.username and args.password):
        print('Please provide a username and password')
        return

    with cli_app_session_manager(host=args.host, username=args.username, password=args.password) as cli_app:
        print("\n>>>proceed...\n")
    
        
        if args.command in ['login','logout']:
            return
                 
        elif args.command == 'list':
            cli_app.list_files()
        
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

            cli_app.download_file(file_to_download, folder, save_filename=filename)

if __name__ == '__main__':
    main()
