Here's an example of how you can use the `cli_app/sharefile.py` file to list, upload, download files:


1. List Files:
```
python cli_app/sharefile.py list --username your_username --password your_password 
```

2. Upload a File:
```shell
python cli_app/sharefile.py upload --username your_username --password your_password --file examples/data/test_file1.txt
```
This command will upload the `file.txt` located at `path/to/file.txt` to the file sharing server.

3. Download a File:
```shell
python cli_app/sharefile.py download --username your_username --password your_password --file file.txt --output path/to/save/file.txt
```
This command will download the `file.txt` from the file sharing server and save it to the specified output path (`path/to/save/file.txt` in this example).

**Note**: Replace `your_username` and `your_password` with your actual username and password. Adjust the file paths (`path/to/file.txt` and `path/to/save/file.txt`) according to your system.
