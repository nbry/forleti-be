""" Routes for user/auth-related tasks """
from flask import Blueprint, request, jsonify
from models.user import User

user_api = Blueprint('user_api', __name__)


@user_api.route('/login')
def login():
    """ Handles a request to log in. Authenticates user name and password
    and returns a token. """
    req = request.json
    res = User.authenticate(req.username, req.password)
    return jsonify(res)


@user_api.route('/signup')
def signup():
    """ Handles a request to sign user up for new account. """
    req = request.json
    res = User.signup(req.username, req.password, req.email)
    return jsonify(res)
