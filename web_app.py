import os
import json
import asyncio
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from photolocationfinder import ImageProcessor

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback_secret_key')

import shutil

config_template_path = 'config.json.template'
config_path = 'config.json'

if not os.path.exists(config_path):
    if os.path.exists(config_template_path):
        shutil.copy(config_template_path, config_path)
        print(f"Created {config_path} from {config_template_path}. Please edit it with your actual configuration.")
    else:
        print(f"Error: Neither {config_path} nor {config_template_path} found. Please create a {config_path} file.")
        exit(1)

try:
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
except json.JSONDecodeError:
    print(f"Error: {config_path} file is not valid JSON. Please check its contents.")
    exit(1)

# Check if any config values are placeholder values
placeholder_values = [
    "YOUR_GOOGLE_API_KEY_HERE",
    "PATH_TO_YOUR_GOOGLE_APPLICATION_CREDENTIALS_FILE",
    "PATH_TO_YOUR_IMAGE_DIRECTORY",
    "YOUR_DATABASE_URL_HERE",
    "YOUR_SECRET_KEY_HERE"
]

if any(value in config.values() for value in placeholder_values):
    print(f"Warning: {config_path} contains placeholder values. Please edit it with your actual configuration.")

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            processor = ImageProcessor(
                api_key=config['google_api_key'],
                cred_path=config['google_application_credentials_file_path'],
                image_dir=app.config['UPLOAD_FOLDER'],
                prompt_for_confirmation=False
            )
            try:
                result = processor.process_single_image(filepath)
                result['image_url'] = url_for('serve_upload', filename=filename)
                return render_template('result.html', result=result)
            except Exception as e:
                error_message = f"Error processing image: {str(e)}"
                app.logger.error(error_message)
                flash(error_message)
                return render_template('upload.html', error=error_message)
    return render_template('upload.html')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
