""" Routes for user profile-related tasks """
import flask_praetorian as fp
from flask import jsonify
from project.models import User
from . import user_profile_api_blueprint


@user_profile_api_blueprint.route('/user/<username>')
def get_user_by_username(username):
    """
    Search for a user by username.
    If matching user is found, return all blog posts made by the user.
    Supply relevant information to load a "profile page". i.e. return the
    user's username and bio as well.
    """
    user = User.lookup(username)
    if user:
        user_blogposts = [{"id": bp.id,
                           "title": bp.title,
                           "content": bp.content,
                           "user_id": bp.user_id,
                           "created": bp.created} for bp in user.blogposts]
        user = {
            "posts": user_blogposts,
            "username": user.username,
            "display_name": user.display_name,
            "bio": user.profile_settings[0].bio,
            "theme": user.profile_settings[0].theme,
            "avatar_url": user.profile_settings[0].avatar_url,
            "header_url": user.profile_settings[0].header_url
        }
        return jsonify({"user": user})
    else:
        message = {
            "status": 404,
            "message": "No User Found"
        }
        return jsonify(message), 404


@user_profile_api_blueprint.route('/home')
@fp.auth_required
def get_logged_in_user_from_header():
    """
    Search for a user by id. This route is not intended to resemble a route
    on the front end. It is primarily used to retrieve a logged in user's
    information. Thus, keep this route as a protected flask praetorian route.

    This route provides "user settings for the logged in user", information
    that will be utilized in the user settings page on the front end.
    """

    user = fp.current_user()

    if user:

        user_blogposts = [{"id": bp.id,
                           "title": bp.title,
                           "content": bp.content,
                           "user_id": bp.user_id,
                           "created": bp.created} for bp in user.blogposts]
        user = {
            "id": user.id,
            "display_name": user.display_name,
            "posts": user_blogposts,
            "username": user.username,
            "email": user.email,
            "bio": user.profile_settings[0].bio,
            "avatar_url": user.profile_settings[0].avatar_url,
            "header_url": user.profile_settings[0].header_url,
            "theme": user.profile_settings[0].theme,
            "dark_mode": user.profile_settings[0].dark_mode
        }
        return jsonify({"user": user})
    else:
        message = {
            "status": 404,
            "message": "No User Found"
        }
        return jsonify(message), 404
