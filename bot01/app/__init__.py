from flask import Flask
from .routes import main  # This imports the 'main' Blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
