""" Routes for user profile-related tasks """
# import flask_praetorian as fp
from flask import jsonify, request
from project.models import BlogPost, User
from . import user_profile_api_blueprint


@user_profile_api_blueprint.route('/<username>')
def get_blogposts_by_username(username):
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
