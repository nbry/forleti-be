from flask import jsonify
from sqlalchemy.exc import IntegrityError

from project.extensions import db


class UserProfileSettings(db.Model):
    __tablename__ = "user_profile_settings"

    # [UTILITY] Provide a getter method. In other words, allow attributes to
    # be retrieved with square bracket notation.
    # e.g. getting a user's username --> user.username OR user['username']
    #
    # NOTE: you still can't assign a new value using bracket notation.
    # For example, if you wanted to change a user's username to 'Jane123',
    # user['username'] = 'Jane123' still won't work. To do this, access the
    # internal __dict__ and modify attributes that way.
    def __getitem__(self, key):
        return self.__dict__[key]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bio = db.Column(db.String(200))
    avatar_url = db.Column(db.Text)
    header_url = db.Column(db.Text)
    theme = db.Column(db.Integer, default=1)
    dark_mode = db.Column(db.Boolean, default=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True)

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
        Changes can only  =be made to bio, avatar_url, header_url, theme, and dark_mode.
        Return a message.
        """
        changeable = ("bio", "avatar_url", "header_url", "theme", "dark_mode")
        if setting not in changeable:
            return jsonify({"message": f"{setting} cannot be in changed"}), 400

        settings = cls.query.filter_by(user_id=user_id).one_or_none()

        # noinspection PyBroadException
        try:
            settings[setting] = change_to
            db.session.commit()
            return jsonify({"message": f"{setting} changed successfully!"}), 200

        except Exception:
            return jsonify({"message": "change could not be submitted"}), 400
