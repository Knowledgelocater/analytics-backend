# import_data.py
import pandas as pd
from sqlalchemy.orm import sessionmaker
from app.models import engine, Data

if __name__ == "__main__":
    import_excel_data("C:/Users/shukl/desktop/Automated-Analutics/analytics-backend/Stock Item with BoM details.xlsx")


def import_excel_data(file_path):
    df = pd.read_excel(file_path)

    Session = sessionmaker(bind=engine)
    session = Session()

    for _, row in df.iterrows():
        data = Data(name=row['Name'], value=row['Value'])
        session.add(data)

    session.commit()
    session.close()
    print("Excel data imported successfully!")
