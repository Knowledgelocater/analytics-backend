from flask import Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
from app.models import engine, Data

# Create a Flask Blueprint
api = Blueprint('api', __name__)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define the /data endpoint
@api.route('/data', methods=['GET'])
def get_data():
    # Query all data from the database
    data = session.query(Data).all()

    # Convert data into JSON
    response = [{'id': d.id, 'name': d.name, 'value': d.value} for d in data]
    return jsonify(response)
