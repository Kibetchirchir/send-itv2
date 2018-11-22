from flask import Flask, jsonify
from instance.config import app_config
from .api.v1 import v1
from .api.v2 import v2
from .db_config import create_tables
from flask_jwt_extended import JWTManager
import os


def create_app(config_name):
    """This method creates the aplication and registers the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['JWT_SECRET_KEY'] = os.getenv('secret') or 'generate-your-own'
    jwt = JWTManager(app)
    create_tables()
    app.register_blueprint(v1)
    app.register_blueprint(v2)

    @app.errorhandler(404)
    def url_doesnt_exist(error):
        return jsonify({
            "Message": "Check your url and ensure it is the correct one as per documentation"
        }), 404
    app.url_map.strict_slashes = False
    return app
