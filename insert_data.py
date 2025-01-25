from sqlalchemy.orm import sessionmaker
from app.models import engine, Data

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample data
sample_data = [
    Data(name="Item 1", value=100.5),
    Data(name="Item 2", value=200.75),
    Data(name="Item 3", value=300.0),
    Data(name="Item 4", value=400.25)
]

# Add data to the session and commit
session.add_all(sample_data)
session.commit()

print("Test data inserted!")
