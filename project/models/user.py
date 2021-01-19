from datetime import datetime

from flask import jsonify
from sqlalchemy.exc import IntegrityError
from project.extensions import db, guard


class User(db.Model):
    __tablename__ = "users"

    # [UTILITY] Provide a getter method. In other words, allow attributes to
    # be retrieved with square bracket notation.
    # e.g. getting a user's username --> user.username OR user['username']
    #
    # NOTE: you still can't assign a new value using bracket notation.
    # For example, if you wanted to change a user's username to 'Jane123',
    # user['username'] = 'Jane123' still won't work. To do this, access the
    # use setattr method (i.e. setattr(user, 'username', 'Jane123)
    def __getitem__(self, key):
        return self.__dict__[key]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    display_name = db.Column(db.String(50))
    hashed_password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    roles = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    blogposts = db.relationship("BlogPost",
                                order_by="desc(BlogPost.created)",
                                cascade="all, delete",
                                backref="user",
                                lazy=True)

    profile_settings = db.relationship("UserProfileSettings",
                                       cascade="all, delete",
                                       backref="user",
                                       lazy=True)

    # *****************************
    # REQUIRED PROPERTIES AND METHODS BY FLASK PRAETORIAN:
    # *****************************

    @property
    def identity(self):
        """
        REQUIRED PROPERTY BY FLASK PRAETORIAN:
        Provides unique id of the user instance.
        """
        return self.id

    # noinspection PyBroadException
    @property
    def rolenames(self):
        """
        REQUIRED PROPERTY BY FLASK PRAETORIAN:
        Provides a list of strings that describe the roles attached to the user instance.
        """
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        """
        REQUIRED PROPERTY BY FLASK PRAETORIAN:
        Provides hashed password assigned to user instance.
        """
        return self.hashed_password

    @classmethod
    def lookup(cls, username: str):
        """
        REQUIRED METHOD BY FLASK PRAETORIAN:
        Returns a user instance if there is one that matches username
        or None if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def lookup_by_email(cls, email: str):
        """
        Returns a user instance if there is one that matches email
        or None if there is not.
        """
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def identify(cls, user_id: int):
        """
        REQUIRED METHOD BY FLASK PRAETORIAN:
        Returns a user instance if there is one that matches id
        or None if there is not.
        """
        return cls.query.get(user_id)

    # *****************************
    # API-related methods:
    # *****************************

    @classmethod
    def signup(cls, username: str, raw_pass: str, email: str):
        """
        Register user for an account w/hashed password.
        Ensure unique username and email.
        Return user.
        """
        hashed_pass = guard.hash_password(raw_pass)
        display_name = f"{username}'s Blog"
        new_user = cls(username=username,
                       hashed_password=hashed_pass,
                       email=email,
                       display_name=display_name)

        db.session.add(new_user)

        try:
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def change_account_setting(cls, setting: str, change_to: str, username: str, password: str):
        """
         Authenticate user. If successful, change requested account setting.
         Sanitize request object by check to see if setting is allowed to be changed.
         Changes can only be made to username, display name, or password.
         NOTE: Changes to email won't be supported until an email verification
         system is set up. Return a message.
        """
        changeable = ("username", "display_name", "password")
        if setting not in changeable:
            return jsonify({"message": f"{setting} cannot be in changed"}), 400

        user = guard.authenticate(username, password)

        # noinspection PyBroadException
        try:
            setattr(user, setting, change_to)
            db.session.commit()
            return jsonify({"message": f"{setting} changed successfully!"}), 200

        except Exception:
            return jsonify({"message": "change could not be submitted"}), 400

    @classmethod
    def remove_account(cls, username, password):
        """
        Authenticate user from token with password provided in request data. If
        successful, remove the user from the database.
        """
        user = guard.authenticate(username, password)

        # noinspection PyBroadException
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "success"}), 200

        except IntegrityError:
            return jsonify({"message": "could not delete user"}), 400
