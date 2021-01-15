# WHEN ADDING A NEW FILE/BLUEPRINT TO THIS, THE ROUTES PACKAGE,
# YOU MUST DO THE FOLLOWING:
# 1. In this file, add the blueprint of the routes under the list
# 2. Add the route file name (the name of the .py file) at the bottom of the page
# 3. Go to __init__.py of the projects directory, and import the blueprint
# 4. Under the register_blueprint(app) method, use the flask register_blueprint method
#    to register the blueprint to the app context.
# You MUST follow all these guidelines to get your route working. Try to follow along
#    with the current code patterns.

from flask import Blueprint

# LIST BLUEPRINTS HERE:
user_auth_api_blueprint = Blueprint('user_auth_api', __name__)
user_profile_api_blueprint = Blueprint('user_profile_api', __name__)
user_settings_api_blueprint = Blueprint('user_settings_api', __name__)
blogpost_api_blueprint = Blueprint('blogpost_api', __name__)

# THIS LINE MUST BE BELOW BLUEPRINTS TO PROVIDE CONTEXT TO ROUTE FILES:
from project.routes import blogpost, user_auth, user_profile_page, user_settings
