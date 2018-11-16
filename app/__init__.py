from flask import Flask, jsonify
from instance.config import app_config
from .api.v1 import v1


def create_app(config_name):
    """This method creates the aplication and registers the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(v1)

    @app.errorhandler(404)
    def url_doesnt_exist(error):
        return jsonify({
            "Message": "Check your url and ensure it is the correct one as per documentation"
        }), 404
    app.url_map.strict_slashes = False
    return app
