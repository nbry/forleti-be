""" Routes for user settings-related tasks """
import flask_praetorian as fp
from flask import jsonify

from . import user_settings_api_blueprint


@user_settings_api_blueprint.route('/settings')
def settings_menu():
    """
    Return a list of settings options.
    To be used as a menu for the settings page.
    """

    # TO BE CHANGED. SHOW MENU THAT DYNAMICALLY REPRESENTS SETTINGS TABLE
    # FOR NOW, ONLY ACCOUNT SETTINGS CAN BE CHANGED
    return jsonify({"settings": ["account"]})


@user_settings_api_blueprint.route('/settings/account')
@fp.auth_required
def account_settings():
    """
    Identify user from JWT, and show current user account settings.
    """
    u = fp.current_user()

    return jsonify({
        "username": u.username,
        "email": u.email,
    })
