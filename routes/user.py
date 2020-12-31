""" Routes for user/auth-related tasks """
import flask_praetorian as fp
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

    req = request.json
    user = guard.authenticate(
        req.get('username', None),
        req.get('password', None)
    )

    if user:
        message = {
            "message": f"Success! Logged in to {user.username}'s account",
            "token": guard.encode_jwt_token(user)
        }
        return jsonify(message)
    else:
        # REMOVE/CHANGE AT PRODUCTION
        return jsonify("Something went wrong. Origin: routes/user.py: login()")


@user_api.route('/signup', methods=['POST'])
def signup():
    """
    Handles a request to sign user up for new account. If successful,
    returns a token.
    """
    req = request.json
    new_user = User.signup(
        req.get('username', None),
        req.get('password', None),
        req.get('email', None)
    )

    # TO BE IMPLEMENTED:
    # 1. ERROR HANDLING FOR DUPLICATE ACCOUNT
    # 2. ERROR HANDLING FOR DUPLICATE EMAIL

    if new_user:
        message = {
            "message": f"Successfully created account for {new_user.username}",
            "token": guard.encode_jwt_token(new_user)
        }
        return jsonify(message)
    else:
        # REMOVE/CHANGE AT PRODUCTION
        return jsonify("Something went wrong. Origin: routes/user.py: signup()")


# *****************************
# TESTING ROUTES:
# REMOVE/CHANGE AT PRODUCTION
# *****************************
@user_api.route("/protected")
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

