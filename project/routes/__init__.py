from flask import Blueprint

# LIST BLUEPRINTS HERE:
user_auth_api_blueprint = Blueprint('user_auth_api', __name__)
user_profile_api_blueprint = Blueprint('user_profile_api', __name__)
user_settings_api_blueprint = Blueprint('user_settings_api', __name__)
blogpost_api_blueprint = Blueprint('blogpost_api', __name__)

# THIS LINE MUST BE BELOW BLUEPRINTS TO PROVIDE CONTEXT TO ROUTE FILES:
from project.routes import user_auth, blogpost, user_settings
