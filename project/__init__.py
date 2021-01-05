from flask import Flask
from project.models.user import User

# Blueprints
from project.routes import user_api_blueprint
from project.routes import blogpost_api_blueprint

# Extensions:
from project.extensions import db, guard


# *****************************
# APPLICATION FACTORY
# *****************************

def create_app(config_file=None):
    """
    Create instance of a Flask app with configurations based on a provided
    file as an argument. Returns the app
    """

    # Create Flask App Instance
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_file)

    # Bind Extensions and Blueprints
    initialize_extensions(app)
    register_blueprints(app)

    return app


# *****************************
# INITIALIZING EXTENSIONS
# *****************************

def initialize_extensions(app, user_model=User):
    """
    Pass Flask extensions to an instantiated Flask app.
    """

    db.init_app(app)
    guard.init_app(app, user_model)


# *****************************
# REGISTERING BLUEPRINTS
# *****************************

def register_blueprints(app):
    """
    Register all blueprints to an instantiated Flask application.
    """
    app.register_blueprint(user_api_blueprint)
    app.register_blueprint(blogpost_api_blueprint)
