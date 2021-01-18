""" Routes for user settings-related tasks """
import flask_praetorian as fp
from flask import jsonify

from . import user_settings_api_blueprint


@user_settings_api_blueprint.route('/settings')
@fp.auth_required
def get_user_settings():
    """
    Get currently logged in user and return settings dictionary
    """

    user = fp.current_user()

    if user:
        # noinspection PyBroadException
        try:
            settings = {
                "username": user.username,
                "email": user.email,
                "bio": user.profile_settings[0].bio,
                "avatar_url": user.profile_settings[0].avatar_url,
                "header_url": user.profile_settings[0].header_url,
                "theme": user.profile_settings[0].theme,
                "dark_mode": user.profile_settings[0].dark_mode
            }

            return jsonify({"settings": settings})

        except Exception:
            return jsonify({"message": "Something went wrong."})
