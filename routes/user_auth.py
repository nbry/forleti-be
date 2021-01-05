""" Routes for user auth-related tasks """
import flask_praetorian as fp
from flask import Blueprint, request, jsonify
from connect_models import guard
from models.user import User

user_auth_api = Blueprint('user_api', __name__)


@user_auth_api.route('/login', methods=['POST'])
def login():
    """
    Handles a request to log in. Authenticates user name and password
    and returns a token.
    """
    req = request.json

    # Authenticate using Praetorian's built in method. Returns None if authentication unsuccessful
    user = guard.authenticate(
        req.get('username', None),
        req.get('password', None)
    )

    # If successfully authenticated, return a message and a JWT
    if user:
        message = {
            "message": f"Success! Logged in to {user.username}'s account",
            "token": guard.encode_jwt_token(user)
        }
        return jsonify(message)

    # If not, return an appropriate auth message message.
    # Theoretically, this code shouldn't run because Praetorian's built in method should
    # handle it for you. Keeping it as a catch all.
    else:
        message = {"message": "Authentication failed."}
        return jsonify(message), 401


@user_auth_api.route('/signup', methods=['POST'])
def signup():
    """
    Handles a request to sign user up for new account. If successful,
    returns a token.
    """
    req = request.json

    # Sign Up for user using information from the request
    new_user = User.signup(
        req.get('username', None),
        req.get('password', None),
        req.get('email', None)
    )

    # If successfully created, return a message and a JWT
    if new_user:
        message = {
            "message": f"Successfully created account for {new_user.username}",
            "token": guard.encode_jwt_token(new_user)
        }
        return jsonify(message)

    # Duplicate account handling, if new_user is None...
    else:
        message = {"message": "User with that username/email already exists!"}
        return jsonify(message), 400


# USER LOG OUT ROUTE (GET)? SHOULD THIS EVEN BE IMPLEMENTED? JWT'S SHOULD THEORETICALLY
# BE STATELESS


# *****************************
# TESTING ROUTES:
# REMOVE/CHANGE AT PRODUCTION
# *****************************
@user_auth_api.route("/protected")
@fp.auth_required
def protected():
    # REMOVE/CHANGE AT PRODUCTION
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return jsonify(
        message="protected endpoint (allowed user {})".format(
            fp.current_user().username,
        )
    )