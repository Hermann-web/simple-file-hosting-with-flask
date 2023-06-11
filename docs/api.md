# Api documentation

## Summary
Here are some examples of how you can access the API routes using cURL commands:
```
# Login
curl -X POST -H "Content-Type: application/json" -d '{"username": "<username>", "password": "<password>"}' http://localhost:5000/api/login

# Upload a file
curl -X POST -F "file=@/path/to/file.txt" -b "session=<session_cookie>" http://localhost:5000/api/upload

# Get the list of files
curl -b "session=<session_cookie>" http://localhost:5000/api/

# Download a file
curl -b "session=<session_cookie>" http://localhost:5000/api/uploads/filename.txt --output filename.txt

# Logout
curl -b "session=<session_cookie>" http://localhost:5000/api/logout
```



## Detailed examples
Here are the examples of how you can access the API routes using cURL commands with more details:

### Login:
```shell
curl -X POST -H "Content-Type: application/json" -d '{"username": "<username>", "password": "<password>"}' http://localhost:5000/api/login
```

### Others
The authentication mechanism uses session-based authentication rather than token-based authentication.

To access the API routes using session-based authentication, you need to include the session cookie in subsequent requests. The session cookie is automatically stored by the browser and sent along with each request.

cURL commands to access the API routes using session-based authentication:

1. Upload a file:
```shell
curl -X POST -F "file=@/path/to/file.txt" -b "session=<session_cookie>" http://localhost:5000/api/upload
```
Replace `/path/to/file.txt` with the actual path to the file you want to upload. Include the session cookie (`session=<session_cookie>`) obtained from the login response in the `-b` parameter.

2. Get the list of files:
```shell
curl -b "session=<session_cookie>" http://localhost:5000/api/
```
Include the session cookie (`session=<session_cookie>`) obtained from the login response in the `-b` parameter.

3. Download a file:
```shell
curl -b "session=<session_cookie>" http://localhost:5000/api/uploads/filename.txt --output filename.txt
```
Replace `filename.txt` with the name of the file you want to download. Include the session cookie (`session=<session_cookie>`) obtained from the login response in the `-b` parameter.

4. Logout:
```shell
curl -b "session=<session_cookie>" http://localhost:5000/api/logout
```
Include the session cookie (`session=<session_cookie>`) obtained from the login response in the `-b` parameter.

Make sure to replace `<username>`, `<password>`, and `<session_cookie>` with the actual values you received from the login response.

Please note that session-based authentication relies on cookies, which are automatically managed by the browser. Therefore, the above cURL commands may not work directly from the command line. Instead, you can use tools like Postman or write scripts in a programming language (e.g., Python using the `requests` library) to perform API requests with session-based authentication."""
