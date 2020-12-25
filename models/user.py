from connect_models import db, guard
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    hashed_password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    roles = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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
        """ Register user for an account w/hashed password.
        Ensure unique username and email.
        Return user. """

        hashed_pass = cls.hash_pass(raw_pass)
        new_user = cls(username=username, hashed_pass=hashed_pass, email=email)
        db.session.add(new_user)

        try:
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()
            return cls.check_for_duplicate_acct(username, email)

    @classmethod
    def hash_pass(cls, pwd: str):
        """ Hash a new password """

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return hashed_utf8

    @classmethod
    def authenticate(cls, username: str, password: str):
        """ Ensure user exists. Check for correct password. Return user."""

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None

    def __repr__(self):
        return f'<User {self.get("username", None)}>'
