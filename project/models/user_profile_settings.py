from flask import jsonify
from sqlalchemy.exc import IntegrityError

from project.extensions import db


class UserProfileSettings(db.Model):
    __tablename__ = "user_profile_settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bio = db.Column(db.String(200))
    avatar_url = db.Column(db.Text)
    header_url = db.Column(db.Text)
    theme = db.Column(db.Integer, default=1)
    dark_mode = db.Column(db.Boolean, default=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
        unique=True)

    user = db.relationship("User", backref="profile_settings", lazy=True)

    @classmethod
    def initialize(cls, user_id):
        """
        This method is to be used when a user account is created. Initializes
        a settings profile for the user with default values.
        """
        new_user_settings = cls(user_id=user_id)
        db.session.add(new_user_settings)

        try:
            db.session.commit()
            return new_user_settings
        except IntegrityError:
            db.session.rolback()
            return None

    @classmethod
    def update_settings(cls, setting: str, change_to, user_id: int):
        """
        Change requested profile setting.
        Sanitize request object by check to see if setting is allowed to be changed.
        Keep this function EXPLICIT to ensure safety. Changes can only
        be made to bio, avatar_url, header_url, theme, and dark_mode.
        Return a message.
        """
        changeable = ("bio", "avatar_url", "header_url", "theme", "dark_mode")
        if setting not in changeable:
            return jsonify({"message": f"{setting} cannot be in changed"}, 400)

        settings = cls.query.filter_by(user_id=user_id).one_or_none()
        # noinspection PyBroadException
        try:
            # Again, keep this function explicit. Make separate conditionals for each
            # change.  Do not use a loop (for now)
            if setting == "bio":
                settings.bio = change_to
                db.session.commit()
                return jsonify({"message": f"{setting} changed successfully!"}, 200)

            # IMPLEMENT THESE AS YOU INTRODUCE THE ABILITY TO CHANGE:

            # elif setting == "avatar_url":
            #     settings.avatar_url = change_to
            #     db.session.commit()
            #     return jsonify({"message": f"{setting} changed successfully!"}, 200)
            #
            # elif setting == "header_url":
            #     settings.header_url = change_to
            #     db.session.commit()
            #     return jsonify({"message": f"{setting} changed successfully!"}, 200)
            #
            # elif setting == "theme":
            #     settings.theme = change_to
            #     db.session.commit()
            #     return jsonify({"message": f"{setting} changed successfully!"}, 200)
            #
            # elif setting == "dark_mode":
            #     settings.dark_mode = change_to
            #     db.session.commit()
            #     return jsonify({"message": f"{setting} changed successfully!"}, 200)

        except Exception:
            return jsonify({"message": "change could not be submitted"}, 400)
