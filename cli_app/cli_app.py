
import requests
import json
from pathlib import Path


class FileSharingClient:
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        print(f'\n>>>base_url ={base_url}')
        self.base_url = f'{base_url}/api'
        self.session = requests.Session()
        self.is_logged_in = False

    def login(self) -> bool:
        print("\n>>>",end="")
        url = f'{self.base_url}/login'
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'username': self.username, 'password': self.password})
        response = self.session.post(url, data=data, headers=headers)
        print(response.text)
        if response.status_code!=200:
            print(f'Login failed: status_code={response.status_code}')
        
        response_json = json.loads(response.content.decode()) #json.loads(response.text)
        if response_json.get('message') != 'Login successful':
            print(f'Login failed: status_code={response.status_code}')
        
        print('Login successful')
        # print(response_json)
        self.is_logged_in = True
        

    def list_files(self, n=10, order='desc'):
        if not self.is_logged_in: self.login()
        print("\n>>>",end="")
        url = f'{self.base_url}?n={n}&order={order}'
        response = self.session.get(url)
        print(response.text)
        
        if not response.status_code == 200:
            print(f'Failed to retrieve files: status_code={response.status_code}')
            return
        
        files = response.json().get('files')
        if not files:
            print(f'No files found: status_code={response.status_code}')
            return
        
        print('Files:')
        for file in files:
            print(file)
        
        self.files = [elt[0] for elt in files]
        

    def upload_file(self, file_path):
        if not self.is_logged_in: self.login()
        print("\n>>>",end="")
        url = f'{self.base_url}/upload'
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = self.session.post(url, files=files)
            if response.status_code == 200:
                print(f'File uploaded successfully from {file_path}')
                
            else:
                print(f'Failed to upload file from {file_path} : status_code={response.status_code}')
            print(response.text)

    def download_file(self, filename, folder_path, save_filename=''):
        if not self.is_logged_in: self.login()
        print("\n>>>",end="")
        url = f'{self.base_url}/uploads/{filename}'
        response = self.session.get(url)
        
        
        if response.status_code == 404:
            print(f'file "{filename}" not found : status_code={response.status_code}')
            print(response.text)
            return 
        
        if response.status_code != 200:
            print(f'Failed to download file : status_code={response.status_code}')
            return 
        
        if not filename:filename = save_filename
        if not filename: filename = 'output.out'
        saved_path = Path(folder_path)/filename
        
        with open(saved_path, 'wb') as file:
            file.write(response.content)
        print(f'File downloaded and saved to {saved_path.resolve()}')
    
    def download_last_n_files(self, n, folder_path, filename=None):
        if not self.is_logged_in:
            self.login()

        url = f'{self.base_url}/last/{n}/download'
        params = {'filename': filename} if filename else None

        response = self.session.get(url, params=params)
        
        if response.status_code != 200:
            print(f'Failed to download last {n} files: status_code={response.status_code}')
            return
        
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
        else:
            filename = f'last_{n}_files.zip'
        
        saved_path = Path(folder_path) / filename
        with open(saved_path, 'wb') as file:
            file.write(response.content)
        
        print(f'Last {n} files downloaded and saved to {saved_path.resolve()}')

    
    def logout(self):
        if not self.is_logged_in: self.login()
        print("\n>>>",end="")
        url = f'{self.base_url}/logout'
        response = self.session.get(url)
        if response.status_code == 200:
            print('Logout successful')
        else:
            print(f'Logout failed : status_code={response.status_code}')
            print(response.text)

if __name__ == '__main__':
    username = "****" # put your user token here #the one in the .env file
    password = "****" # put your user key here #the one in the .env file
    base_url = "http://localhost:5000"
    # Example usage:
    input_folder = Path('examples/data')
    output_folder = Path('examples/output')
    output_folder.mkdir(exist_ok=True)
    cli_app = FileSharingClient(username=username, password=password, base_url=base_url)
    cli_app.login()
    cli_app.upload_file(input_folder/'test_file1.txt')
    cli_app.download_file('noexistant_file', output_folder)
    cli_app.list_files()
    cli_app.upload_file(input_folder/'test_file2.txt')
    cli_app.download_file('test_file2.txt', output_folder)
    cli_app.list_files()
    cli_app.download_last_n_files(5, output_folder)
    cli_app.logout()
