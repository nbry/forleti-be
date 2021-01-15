""" Routes for user profile-related tasks """
import flask_praetorian as fp
from flask import jsonify, request
from project.models import User
from . import user_profile_api_blueprint
from project.extensions import guard


@user_profile_api_blueprint.route('/<username>')
def get_user_by_username(username):
    """
    Search for a user by username.
    If matching user is found, return all blog posts made by the user.
    Supply relevant information to load a "profile page". i.e. return the
    user's username and bio as well.
    """
    res = User.lookup(username)
    if res:
        user = {
            "posts": res.posts,
            "username": res.username,
            "bio": res.bio,
        }
        return jsonify({"user": user})


@user_profile_api_blueprint.route('/home')
@fp.auth_required
def get_logged_in_user_from_header():
    """
    Search for a user by id. This route is not intended to resemble a route
    on the front end. It is primarily used to retrieve a logged in user's
    information. Thus, keep this route as a protected flask praetorian route.
    """
    return jsonify({"hello": "world"})
    # token = request.headers.get("Authorization")
    # import ipdb;
    # ipdb.set_trace()
    # user = guard.get_user_from_registration_token(token)
    #
    # if user:
    #     user = {
    #         "posts": user.posts,
    #         "username": user.username,
    #         "bio": user.bio,
    #     }
    #     return jsonify({"user": user})
