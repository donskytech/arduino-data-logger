import os
from flask import Flask, render_template
from config import Config  
import logging
from flask import request, jsonify
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from app.extensions import mongo

API_PATH_PREFIX = '/api/'

### Application Factory ###
def create_app():

    app = Flask(__name__)

    # Configure the flask app instance
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    # Register blueprints
    register_blueprints(app)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)
    
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app


### Helper Functions ###
def register_blueprints(app):
    # from app.auth import auth_blueprint
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.commands import commands_bp
    app.register_blueprint(commands_bp)

def initialize_extensions(app):
    mongo.init_app(app)

def register_error_handlers(app):

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        if API_PATH_PREFIX in request.path:
            return jsonify({"error": True, "message": f"Invalid POST Request!"})
        return render_template('400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        if API_PATH_PREFIX in request.path:
            return jsonify({"error": True, "message": f"Error processing API request!"})
        return render_template('500.html'), 500
    
   

def configure_logging(app):

    # Deactivate the default flask logger so that log messages don't get duplicated 
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler('app.log', maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)