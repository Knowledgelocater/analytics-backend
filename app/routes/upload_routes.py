import os
from flask import Blueprint, request, jsonify
from app.models import UploadedData, Session
from flask import render_template



upload_blueprint = Blueprint('upload', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_blueprint.route('/upload-form', methods=['GET'])
def upload_form():
    return render_template('upload_form.html')


@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200
