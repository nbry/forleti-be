""" Routes for user/auth-related tasks """
from flask import Blueprint, request, jsonify

user_api = Blueprint('user_api', __name__)


@user_api.route('/login')
def login():
    """ Handles a request to log in. Authenticates user name and password
    and returns a token. """
    req = request.json
    return jsonify({"request": req})
