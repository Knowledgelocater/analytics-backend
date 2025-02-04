import os
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
from urllib.parse import quote_plus

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "Krishna@108",
    database="analytics_db"
)
cursor = conn.cursor()

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

    # ✅ Insert Data into MySQL Database
    table_name = os.path.splitext(latest_file)[0]  # Use filename as table name

        # Create SQLAlchemy engine
    password = quote_plus("Krishna@108")
    DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/analytics_db"
    engine = create_engine(DATABASE_URL)


    df.to_sql(name=table_name, con=engine, if_exists="append", index=False, dtype=None)
    print(f"Data from {latest_file} has been successfully uploaded to the database.")
