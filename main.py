from flask import Flask
from app.routes.upload_routes import upload_blueprint

app = Flask(__name__)
app.register_blueprint(upload_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
