# File Sharing API Documentation

## Summary

This document provides details on accessing the File Sharing API routes using cURL commands. It includes examples for login, uploading, listing files, downloading files, and logout.

## Updates

### 2024/02/10

- Added usage of the `n` and `order` parameters for listing files.
- Introduced an endpoint to download the last N files.

## Detailed Examples

### Login

To authenticate and obtain a session cookie for subsequent requests:

```shell
curl -X POST -H "Content-Type: application/json" -d '{"username": "<username>", "password": "<password>"}' http://localhost:5000/api/login
```

### Uploading a File

To upload a file to the server:

```shell
curl -X POST -F "file=@/path/to/file.txt" -b "session=<session_cookie>" http://localhost:5000/api/upload
```

Replace `/path/to/file.txt` with the actual path to the file you want to upload. Include the session cookie (`session=<session_cookie>`) obtained from the login response in the `-b` parameter.

### Listing Files

To list files from the server with optional parameters `n` and `order`:

```shell
curl -b "session=<session_cookie>" http://localhost:5000/api/?n=<n>&order=<order>
```

Replace `<n>` with the number of files you want to list (optional, default is 10) and `<order>` with the order of listing (`asc` or `desc`, optional, default is `desc`). Include the session cookie (`session=<session_cookie>`) obtained from the login response in the `-b` parameter.

### Downloading a File

To download a specific file from the server:

```shell
curl -b "session=<session_cookie>" http://localhost:5000/api/uploads/filename.txt --output filename.txt
```

Replace `filename.txt` with the name of the file you want to download. Include the session cookie (`session=<session_cookie>`) obtained from the login response in the `-b` parameter.

### Downloading the Last N Files

To download the last N files from the server:

```shell
curl -b "session=<session_cookie>" http://localhost:5000/api/last/<n>/download --output last_files.zip
```

Replace `<n>` with the number of files you want to download. Include the session cookie (`session=<session_cookie>`) obtained from the login response in the `-b` parameter.

### Logout

To logout and end the session:

```shell
curl -b "session=<session_cookie>" http://localhost:5000/api/logout
```

Include the session cookie (`session=<session_cookie>`) obtained from the login response in the `-b` parameter.

Make sure to replace `<username>`, `<password>`, `<session_cookie>`, `<n>`, and `<order>` with the actual values you received from the login response.

Please note that session-based authentication relies on cookies, which are automatically managed by the browser. Therefore, the provided cURL commands may not work directly from the command line. Instead, consider using tools like Postman or writing scripts in a programming language (e.g., Python using the `requests` library) to perform API requests with session-based authentication.
