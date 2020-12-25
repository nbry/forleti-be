""" Routes for user/auth-related tasks """
from flask import Blueprint, request, jsonify
from connect_models import guard
from models.user import User

user_api = Blueprint('user_api', __name__)


@user_api.route('/login', methods=['POST'])
def login():
    """
    Handles a request to log in. Authenticates user name and password
    and returns a token.
    """

    import ipdb;ipdb.set_trace()
    req = request.json
    user = guard.authenticate(
        req.get('username', None),
        req.get('password', None)
    )

    if user:
        message = {
            "message": f"Success! Logged in to {user.username}'s account"
        }
        return jsonify(message)
    else:
        # REMOVE/CHANGE AT PRODUCTION
        return jsonify("Something went wrong. Origin: routes/user.py: login()")


@user_api.route('/signup', methods=['POST'])
def signup():
    """
    Handles a request to sign user up for new account.
    """
    req = request.json
    new_user = User.signup(
        req.get('username', None),
        req.get('password', None),
        req.get('email', None)
    )

    if new_user:
        message = {
            "message": f"Successfully created account for {new_user.username}"
        }
        return jsonify(message)
    else:
        # REMOVE/CHANGE AT PRODUCTION
        return jsonify("Something went wrong. Origin: routes/user.py: signup()")
