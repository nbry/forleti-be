import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from routes.user import user_api
from flask_debugtoolbar import DebugToolbarExtension

# *****************************
# APP CONFIGURATION
# *****************************
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///nathan'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', "EIJALWIEJAEFIJ320F23F8SEF209238FDI")
toolbar = DebugToolbarExtension(app)

# Connect Flask app to database
db = SQLAlchemy()
db.app = app
db.init_app(app)

# Register blueprints from routes folder
app.register_blueprint(user_api)


@app.route('/test')
def hello_world():
    return jsonify({"message": "hello world"})

# # IF RUNNING ON PYCHARM:
# if __name__ == '__main__':
#     app.run()
