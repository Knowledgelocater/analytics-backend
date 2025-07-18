import time
import requests
import os
import json

# ✅ Use an absolute path for reliability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_PATH = os.path.join(BASE_DIR, "../../uploads/")
API_URL = "http://localhost:5000/api/upload"
PROCESSED_FILES_PATH = os.path.join(BASE_DIR, "processed_files.json")

# ✅ Function to load processed files from JSON
def load_processed_files():
    if os.path.exists(PROCESSED_FILES_PATH):
        with open(PROCESSED_FILES_PATH, "r") as f:
            return set(json.load(f))
    return set()

# ✅ Function to save processed files to JSON
def save_processed_files(processed_files):
    with open(PROCESSED_FILES_PATH, "w") as f:
        json.dump(list(processed_files), f)

def watch_folder():
    processed_files = load_processed_files()  # Load processed files history
    print(f"📡 Watching folder: {FOLDER_PATH}")

    while True:
        try:
            files = os.listdir(FOLDER_PATH)
            for file in files:
                file_path = os.path.join(FOLDER_PATH, file)

                if file not in processed_files and os.path.isfile(file_path):
                    print(f"🚀 Uploading {file}...")
                    with open(file_path, 'rb') as f:
                        response = requests.post(API_URL, files={'file': f})

                    # ✅ Handle response and errors
                    if response.status_code == 200:
                        print(f"✅ Successfully uploaded: {file}")
                        processed_files.add(file)
                        save_processed_files(processed_files)  # Save progress
                    else:
                        print(f"❌ Error uploading {file}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"⚠ Network error: {e}")

        except Exception as e:
            print(f"⚠ Unexpected error: {e}")

        time.sleep(5)  # Check for new files every 5 seconds

if __name__ == "__main__":
    watch_folder()
