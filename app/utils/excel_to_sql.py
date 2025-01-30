import os
import pandas as pd

# ✅ Set the correct uploads folder path (root directory)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "../../uploads")  # Adjusted path

# ✅ Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ✅ Get all .csv and .xlsx files
excel_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith((".csv", ".xlsx"))]

# ✅ Check if any files are present
if not excel_files:
    print("No CSV or Excel files found in the uploads folder.")
else:
    # ✅ Get the latest uploaded file
    latest_file = max(excel_files, key=lambda f: os.path.getmtime(os.path.join(UPLOAD_FOLDER, f)))
    file_path = os.path.join(UPLOAD_FOLDER, latest_file)

    # ✅ Load the data
    if latest_file.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    print(f"Loaded file: {latest_file}")
    print(df.head())
