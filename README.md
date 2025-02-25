# Automated Analytics Backend

This repository contains the backend code for the Automated Analytics project. The backend is built using Flask, a lightweight WSGI web application framework in Python.

## Prerequisites

To run the `main.py` file, ensure you have the following installed:

1. **Python 3.6+**: Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).
2. **Flask**: Install Flask using pip:
    ```sh
    pip install Flask
    ```
3. **Other Dependencies**: Install other dependencies listed in `requirements.txt` (if available):
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/Automated-Analytics.git
    cd Automated-Analytics/analytics-backend
    ```

2. **Run the Flask application**:
    ```sh
    python main.py
    ```

3. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:5000/`.

## File Overview

- `main.py`: The main entry point of the Flask application.
- `app/routes/upload_routes.py`: Contains the blueprint for handling file uploads.
- `templates/upload_form.html`: The HTML template for the upload form.

## License

This project is licensed under the MIT License.

## How `main.py` Works

The `main.py` file initializes the Flask application, sets up the routes, and renders the HTML templates. It handles incoming requests and processes data accordingly.

### Key Functions in `main.py`:

1. **Initialization**:
    ```python
    from flask import Flask
    app = Flask(__name__)
    ```

2. **Route Setup**:
    ```python
    from app.routes.upload_routes import upload_blueprint
    app.register_blueprint(upload_blueprint)
    ```

3. **Running the Application**:
    ```python
    if __name__ == "__main__":
        app.run(debug=True)
    ```

### Handling Requests and Rendering Templates:

- The `main.py` file uses the routes defined in `app/routes/upload_routes.py` to handle file uploads.
- It renders the `upload_form.html` template to provide a user interface for uploading files.

By following these steps, `main.py` ensures that the application is properly initialized, routes are set up, and templates are rendered to handle user interactions.

## Handling File Uploads

The `upload_routes.py` file contains the blueprint for handling file uploads. It includes routes for rendering the upload form and processing the uploaded files.It ensures that file got uploaded into uploads folder.

### Functionality

Runs a Flask API that handles file uploads.
Saves uploaded files to a local uploads folder.
Reads CSV or Excel files and inserts data into a MySQL database.
Returns JSON responses with success or error messages.

### Key Components

Defines Flask API endpoints:
/upload-form: Serves an HTML form for manual uploads.
/upload: Handles actual file uploads (via POST requests).
Saves uploaded files using file.save().
Reads CSV/Excel files into Pandas DataFrames.
Inserts data into MySQL using SQLAlchemy (to_sql()).

### Role

 Acts as a backend server that receives, processes, and stores uploaded files.

#### Key Functions in `upload_routes.py`:

1. **Upload Form Route**:
    ```python
    @upload_blueprint.route('/upload-form', methods=['GET'])
    def upload_form():
        """Render the HTML upload form."""
        return render_template('upload_form.html')
    ```

2. **File Upload Route**:
    ```python
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
    ```

By following these steps, `upload_routes.py` ensures that the application can handle file uploads, save them to the uploads folder.

## Watch Folder Script

The `watch_folder.py` script monitors a specified folder for new files and uploads them to a specified API endpoint. This script is useful for automating the process of uploading files as soon as they are added to the folder.

### Role

Acts as a client that automates file uploads to a remote API.

### Key Components

Uses os.listdir() to check files in "../../uploads/".
Sends files using requests.post().
Uses a set (processed_files) to track already uploaded files.
Runs indefinitely with time.sleep(5), checking for new files.

### Functionality

It monitors a local folder (uploads/).
When a new file appears, it automatically uploads it to an API (http://localhost:5000/api/upload).
It sends the file using an HTTP request (requests.post()).
Runs continuously in a loop, checking every 5 seconds for new files.

### How `watch_folder.py` Works

The script continuously checks the folder for new files and uploads them to the API endpoint.

### Key Functions in `watch_folder.py`:

1. **Folder Monitoring**:
    ```python
    import time
    import os

    FOLDER_PATH = "../../uploads/"
    processed_files = set()

    while True:
        files = os.listdir(FOLDER_PATH)
        for file in files:
            if file not in processed_files:
                print(f"Uploading {file}...")
                processed_files.add(file)
        time.sleep(5)  # Check for new files every 5 seconds
    ```

2. **File Upload**:
    ```python
    import requests

    API_URL = "http://localhost:5000/api/upload"

    def upload_file(file_path):
        with open(file_path, 'rb') as f:
            response = requests.post(API_URL, files={'file': f})
            print(response.json())
    ```

3. **Combining Monitoring and Upload**:
    ```python
    def watch_folder():
        processed_files = set()

        while True:
            files = os.listdir(FOLDER_PATH)
            for file in files:
                if file not in processed_files:
                    print(f"Uploading {file}...")
                    upload_file(os.path.join(FOLDER_PATH, file))
                    processed_files.add(file)
            time.sleep(5)  # Check for new files every 5 seconds

    watch_folder()
    ```

By following these steps, `watch_folder.py` ensures that any new files added to the folder are automatically uploaded to the specified API endpoint.
