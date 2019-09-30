from flask import Flask
from flask_cors import CORS

from pokedex.api import register_api


def create_app():
    app = Flask(__name__)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True

    CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

    register_api(app)

    return app
