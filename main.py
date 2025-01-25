from flask import Flask
from app.routes.api import api  # Import the blueprint from the correct path

# Initialize the Flask app
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api, url_prefix='/api')

# Define a test route (optional)
@app.route('/')
def home():
    return "Welcome to the Analytics Backend!"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
