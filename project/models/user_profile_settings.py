from flask import jsonify

from project.extensions import db


class UserProfileSettings(db.Model):
    __tablename__ = "user_profile_settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bio = db.Column(db.String(200))
    avatar_url = db.column(db.Text)
    header_url = db.column(db.Text)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False)

    user = db.relationship("User", backref="profile_settings", lazy=True)

    @classmethod
    def update_setting(cls, user_id, settings: dict):
        """
        Update profile settings provided with information provided
        in a dictionary. Settings dictionary can include bio,
        avatar_url, and header_url. Intended to receive data from front
        end after user submits a form to change settings. Returns a dictionary
        or message.
        """
        user_set = cls.query.filter_by(user_id=user_id).one_or_none()

        if user_set:
            # noinspection PyBroadException
            try:
                user_set.bio = settings.get("bio", user_set.bio)
                user_set.avatar_url = settings.get("avatar_url", user_set.avatar_url)
                user_set.header_url = settings.get("header_url", user_set.header_url)
                db.session.commit()

                return user_set

            except Exception:
                db.session.rollback()
                return jsonify({"message": "Could not update settings."})
        else:
            return jsonify({"message": "Something went wrong."})
