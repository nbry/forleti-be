from flask import jsonify

from project.extensions import db


class UserStyleSettings(db.Model):
    __tablename__ = "user_style_settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    background_color = db.Column(db.Text)
    board_color = db.Column(db.Text)
    dark_mode = db.Column(db.Boolean, default=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False)

    user = db.relationship("User", backref="style_settings", lazy=True)

    @classmethod
    def update_setting(cls, user_id, settings: dict):
        """
        Update style settings provided with information provided
        in a dictionary. Settings dictionary can include background_color,
        board_color, and dark_mode. Intended to receive data from front
        end after user submits a form to change settings. Returns a dictionary
        or message.
        """
        user_set = cls.query.filter_by(user_id=user_id).one_or_none()

        if user_set:
            # noinspection PyBroadException
            try:
                user_set.background_color = settings.get("background_color",
                                                         user_set.background_color)
                user_set.board_color = settings.get("board_color",
                                                    user_set.board_color)
                user_set.dark_mode = settings.get("dark_mode",
                                                  user_set.dark_mode)
                db.session.commit()

                return user_set

            except Exception:
                db.session.rollback()
                return jsonify({"message": "Could not update settings."})
        else:
            return jsonify({"message": "Something went wrong."})
