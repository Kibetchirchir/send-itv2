from flask import Flask, Blueprint
from .v1 import v1


def create_app(config_name="development"):
    app = Flask(__name__)
    app.register_blueprint(v1)
    return app
