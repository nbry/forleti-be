""" Routes for user auth-related tasks """
import flask_praetorian as fp
from flask import request, jsonify
from project.extensions import guard
from project.models import User, UserProfileSettings
from . import user_auth_api_blueprint


@user_auth_api_blueprint.route('/login', methods=['POST'])
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


@user_auth_api_blueprint.route('/signup', methods=['POST'])
def signup():
    """
    Handle a request to sign user up for new account. If successful,
    return a token.
    """
    req = request.json
    username = req.get("username", None)
    password = req.get("password", None)
    email = req.get("email", None)

    # Check if password in request is less than 6 characters
    if len(password) < 8 or len(username) < 6:
        return jsonify({"message": "INVALID USERNAME/PASSWORD",
                        "username_constraints": "Username must be unique and between 5 and 15 characters",
                        "password_constraints": "Password must be 8 to 50 characters in length"}
                       ), 400

    # Check to see if there is an existing user
    if User.check_for_duplicate_account(username, email):
        message = {
            "message": "Account already exists with that email/username",
            "status": 400
        }
        return jsonify(message), 400

    # Sign Up for user using information from the request
    new_user = User.signup(username, password, email)

    # Initialize settings profile for new user
    settings = UserProfileSettings.initialize(new_user.id)

    # If successfully created, return a message and a JWT
    if new_user and settings:
        message = {
            "message": f"Successfully created account for {new_user.username}",
            "token": guard.encode_jwt_token(new_user)
        }
        return jsonify(message)

    else:
        message = {"message": "Something went wrong"}
        return jsonify(message), 400


@user_auth_api_blueprint.route('/account/remove', methods=["DELETE"])
@fp.auth_required
def remove_account():
    """
    Get current user from token. Authenticate with password. Return message.
    """
    req = request.json
    user = fp.current_user()
    message = User.remove_account(user.username, req.get("password"))
    return message


# There's probably a better way to do this, but...
@user_auth_api_blueprint.route('/poke')
def poke_server():
    """
    Awaken back end when someone visits the site.
    Some deployed apps can "go to sleep" if there is no traffic.
    """
    return jsonify("Poke you back!")
