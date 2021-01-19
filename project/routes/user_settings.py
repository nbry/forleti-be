""" Routes for user settings-related tasks """
import flask_praetorian as fp
from flask import  request

from . import user_settings_api_blueprint
from project.models import User
from project.models import UserProfileSettings


@user_settings_api_blueprint.route('/settings/change', methods=["POST"])
@fp.auth_required
def change_user_setting():
    """
    This route is to be used when user is submitting a change to their profile
    or account. Changes are submitted through a request. If user is requesting
    an account change (i.e. category="account"), user must provide a password
    and be authenticated. Return a message.
    """
    req = request.json

    if req.get("category") == "account":
        user = fp.current_user()
        message = User.change_account_setting(req.get("setting"), req.get("changeTo"), user.username,
                                              req.get("password"))
        return message

    else:
        user = fp.current_user()
        message = UserProfileSettings.update_settings(req.get("setting"), req.get("changeTo"), user.id)
        return message


# This route is not being utilized at the moment, but keep it
# for future implementation
# @user_settings_api_blueprint.route('/settings')
# @fp.auth_required
# def get_user_settings():
#     """
#     Get currently logged in user and return settings dictionary.
#     """
#
#     user = fp.current_user()
#
#     if user:
#         # noinspection PyBroadException
#         try:
#             settings = {
#                 "username": user.username,
#                 "email": user.email,
#                 "bio": user.profile_settings[0].bio,
#                 "avatar_url": user.profile_settings[0].avatar_url,
#                 "header_url": user.profile_settings[0].header_url,
#                 "theme": user.profile_settings[0].theme,
#                 "dark_mode": user.profile_settings[0].dark_mode
#             }
#
#             return jsonify({"settings": settings})
#
#         except Exception:
#             return jsonify({"message": "Something went wrong."}), 400
