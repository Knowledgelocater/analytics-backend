import time
import requests
import os

FOLDER_PATH = "../../uploads/"
API_URL = "http://localhost:5000/api/upload"

def watch_folder():
    processed_files = set()

    while True:
        files = os.listdir(FOLDER_PATH)
        for file in files:
            if file not in processed_files:
                print(f"Uploading {file}...")
                with open(os.path.join(FOLDER_PATH, file), 'rb') as f:
                    response = requests.post(API_URL, files={'file': f})
                    print(response.json())
                    processed_files.add(file)
        time.sleep(5)  # Check for new files every 5 seconds

watch_folder()