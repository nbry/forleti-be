import os
from flask import Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from connect_models import connect_db
from models.user import User
from routes.user_auth import user_auth_api


app = Flask(__name__)

# *****************************
# APP CONFIGURATION
# *****************************

# Connect to Postgres. For development, change your database name here:
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///forleti_db'))

# Flask/SQLAlchemy debugging settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', "EIJALWIEJAEFIJ320F23F8SEF209238FDI")
toolbar = DebugToolbarExtension(app)

# Flask Praetorian JWT settings:
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}

# Connect Flask app to database and initialize Praetorian
connect_db(app, User)

# Register blueprints from routes folder
app.register_blueprint(user_auth_api)


@app.route('/test')
def hello_world():
    return jsonify({"message": "hello world"})

# # IF RUNNING ON PYCHARM:
# if __name__ == '__main__':
#     app.run()
