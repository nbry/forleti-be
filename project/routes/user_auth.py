""" Routes for user auth-related tasks """
import flask_praetorian as fp
from flask import request, jsonify
from project.extensions import guard
from project.models import User
from . import user_api_blueprint


@user_api_blueprint.route('/login', methods=['POST'])
def login():
    """
    Handle a request to log in. Authenticate user name and password
    and return a token.
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

    # If not, return an appropriate auth message.
    # Theoretically, this code shouldn't run because Praetorian's authenticate method should
    # handle it for you. Keeping it as a catch all.
    else:
        message = {"message": "Authentication failed."}
        return jsonify(message), 401


@user_api_blueprint.route('/signup', methods=['POST'])
def signup():
    """
    Handle a request to sign user up for new account. If successful,
    return a token.
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
@user_api_blueprint.route("/protected")
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


@user_api_blueprint.route('/test')
def hello_world():
    return jsonify({"message": "hello world"})
