from datetime import datetime
import json
import os
import mimetypes
from slugify import slugify
from flask import Flask, render_template, request, redirect, send_from_directory
from flask import session, jsonify
from flask import url_for, Response
import constants


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = constants.UPLOAD_FOLDER
app.config['DATA_FILE'] = constants.DATA_FILE
app.config['SECRET_KEY'] = constants.FLASK_SECRET_KEY
app.config['DEBUG'] = constants.DEBUG
app.config['USERNAME'] = constants.USERNAME
app.config['PASSWORD'] = constants.PASSWORD

print(app.config['DATA_FILE'], type(app.config['DATA_FILE']))

def validate_credentials(username, password):
    res = (username == app.config['USERNAME'] and password == app.config['PASSWORD'])
    session['logged_in'] = res
    return res

def is_logged_in():
    return 'logged_in' in session and session['logged_in']

@app.route('/')
def index():
    if not is_logged_in():
        return redirect('/login')

    files = get_files_with_dates()
    return render_template('index.html', files=files)

@app.route('/api')
def api_index():
    if not is_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401

    files = get_files_with_dates()
    return jsonify({'files': files})

def get_files_with_dates():
    data = load_data_from_json()
    return [(filename, data[filename]) for filename in sorted(data, key=data.get) if (app.config['UPLOAD_FOLDER']/filename).exists()]

def load_data_from_json():
    if os.path.exists(app.config['DATA_FILE']):
        with open(app.config['DATA_FILE'], 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                pass
    return {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if validate_credentials(username, password):
            return redirect('/')

    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    username = request.json.get('username')
    password = request.json.get('password')

    if validate_credentials(username, password):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/api/logout')
def api_logout():
    session.clear()
    return jsonify({'message': 'Logged out'})


def handle_file_saving(file):
    filename = slugify_filename(file.filename)
    file_save = app.config['UPLOAD_FOLDER'] / filename
    print(f"saving {file_save.resolve()}")
    file.save(file_save)
    update_data_file(filename)
    return filename
    
def slugify_filename(filename):
    # Split the filename and extension
    _ = filename.rsplit('.', 1)
    if len(_)<2: return 
    base, extension = _
    # Slugify the base part
    slug_base = slugify(base)
    # Join the slugified base with the original extension
    slug_filename = f"{slug_base}.{extension}"
    return slug_filename


@app.route('/upload', methods=['POST'])
def upload():
    print("upload route !!")
    if not is_logged_in():
        print('is not logged in')
        return redirect('/')

    file = request.files['file']
    if file:
        filename = handle_file_saving(file)
    return redirect('/')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if not is_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401

    file = request.files['file']
    if file:
        filename = handle_file_saving(file)
        return jsonify({'message': f'File uploaded: {filename}'})
    else:
        return jsonify({'message': 'No file provided'}), 400
        
def update_data_file(filename):
    data = load_data_from_json()
    data[filename] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(app.config['DATA_FILE'], 'w') as file:
        json.dump(data, file)


@app.route('/uploads/<path:filename>')
def download(filename):
    if not is_logged_in():
        print('is not logged in')
        return redirect('/')

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/uploads/<path:filename>')
def api_download(filename):
    if not is_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def get_content_type(file_path):
    # Determine the content type based on the file extension
    mime_type, _ = mimetypes.guess_type(file_path)

    # Map .md and .mmd extensions to text/plain
    if mime_type in ['text/markdown', 'text/x-markdown']:
        mime_type = 'text/plain'
    if file_path.endswith(".md") or file_path.endswith(".mmd"):
        mime_type = 'text/plain'

    return mime_type

@app.route('/open/<path:filename>')
def open_file(filename):
    if not is_logged_in():
        print('is not logged in')
        return redirect('/')

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        return "File not found"

    mime_type = get_content_type(file_path)

    # Map .md and .mmd extensions to text/plain
    if mime_type == 'text/markdown' or mime_type == 'text/x-markdown':
        mime_type = 'text/plain'

    if mime_type:
        with open(file_path, 'rb') as file:
            file_content = file.read()
        return Response(file_content, content_type=mime_type)

    return "Unknown file type"

@app.route('/raw/<path:filename>')
def raw_file(filename):
    if not is_logged_in():
        print('is not logged in')
        return redirect('/')

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        return "File not found"

    with open(file_path, 'rb') as file:
        file_content = file.read()
    return file_content

# Serve static files from the 'static' folder
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run()