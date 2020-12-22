import os
from flask import Flask, jsonify, request
from models import connect_db
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

connect_db(app)


# *****************************
# ROUTES
# *****************************
@app.route('/test')
def hello_world():
    return jsonify({"message": "hello world"})


# AUTH ROUTES:
@app.route('/login')
def login():
    """ Handles a request to log in. Authenticates user name and password
    and returns a token. """
    req = request.json
    return jsonify({"request": request.body})

# # IF RUNNING ON PYCHARM:
# if __name__ == '__main__':
#     app.run()
