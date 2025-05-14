import os
import zlib
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from waitress import serve

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def get_file_size(path):
    """Get the size of the file"""
    try:
        return os.path.getsize(path)
    except:
        return 0

def compress_file(input_path, output_path):
    """Compress the file using zlib"""
    with open(input_path, 'rb') as f:
        data = f.read()
    compressed_data = zlib.compress(data)

    with open(output_path, 'wb') as f:
        f.write(compressed_data)

    # Save the file extension in a separate .ext file
    ext = os.path.splitext(input_path)[1]
    with open(output_path + '.ext', 'w') as f:
        f.write(ext)

def decompress_file(input_path, output_path_base):
    """Decompress the file using zlib"""
    with open(input_path, 'rb') as f:
        compressed_data = f.read()
    decompressed_data = zlib.decompress(compressed_data)

    # Retrieve original file extension
    ext_file = input_path + '.ext'
    if os.path.exists(ext_file):
        with open(ext_file, 'r') as f:
            ext = f.read().strip()
    else:
        ext = '.bin'

    final_output_path = output_path_base + ext
    with open(final_output_path, 'wb') as f:
        f.write(decompressed_data)

    return final_output_path

@app.route('/')
def index():
    """Main route that displays the file upload forms"""
    message = request.args.get('message')  # Optional message for status
    return render_template('index.html', message=message)

@app.route('/compress', methods=['POST'])
def compress():
    """Handle file compression"""
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return redirect(url_for('index', message="No file selected."))

    filename = secure_filename(uploaded_file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    uploaded_file.save(input_path)

    # Compress the file
    output_path = os.path.join(PROCESSED_FOLDER, filename + '.zlib')
    compress_file(input_path, output_path)

    return send_file(output_path, as_attachment=True)

@app.route('/decompress', methods=['POST'])
def decompress():
    """Handle file decompression"""
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return redirect(url_for('index', message="No file selected."))

    filename = secure_filename(uploaded_file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    uploaded_file.save(input_path)

    # Decompress the file
    output_base = os.path.join(PROCESSED_FOLDER, filename)
    output_path = decompress_file(input_path, output_base)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
