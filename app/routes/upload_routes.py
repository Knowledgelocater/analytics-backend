import os
import pandas as pd
from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import create_engine
from app.models import UploadedData, Session
from urllib.parse import quote_plus

upload_blueprint = Blueprint('upload', __name__)

UPLOAD_FOLDER = "uploads/"
password = quote_plus("Krishna@108")
DB_URL = f"mysql+pymysql://root:{password}@localhost:3306/analytics_db"
engine = create_engine(DB_URL)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_blueprint.route('/upload-form', methods=['GET'])
def upload_form():
    """Render the HTML upload form."""
    return render_template('upload_form.html')

@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    """Handles file upload and inserts data into the database."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)  # Save the uploaded file

    # Insert Data into Database
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        table_name = os.path.splitext(file.filename)[0]  # Use filename as table name
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        return jsonify({"message": f"{file.filename} uploaded and data inserted into DB!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500