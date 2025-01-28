from flask import Flask, render_template
from app.routes.upload_routes import upload_blueprint

app = Flask(__name__)
app.register_blueprint(upload_blueprint, url_prefix='/api')

# Define a route for the root URL ("/")
@app.route('/')
def home():
    return render_template('upload_form.html')  # You need to create this 'home.html' file

if __name__ == '__main__':
    app.run(debug=True)
