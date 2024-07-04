import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from photolocationfinder import ImageProcessor

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the image
            processor = ImageProcessor(config['google_api_key'],
                                       config['google_application_credentials_file_path'], 
                                       app.config['UPLOAD_FOLDER'],
                                       False)
            try:
                result = processor.process_single_image(filepath)
                
                # Add the image URL to the result
                result['image_url'] = url_for('serve_upload', filename=filename)
                
                return render_template('result.html', result=result)
            except Exception as e:
                error_message = f"Error processing image: {str(e)}"
                print(error_message)  # Log the error
                flash(error_message)
                return render_template('upload.html', error=error_message)
    return render_template('upload.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
