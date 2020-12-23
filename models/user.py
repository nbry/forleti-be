from connect_models import db
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def signup(cls, username, password, email):
        """ Register user for an account w/hashed password.
        Ensure unique username and email.
        For now, return a message. """
        hashed_pass = cls.hash_pass(password)
        new_user = cls(username=username, password=hashed_pass, email=email)
        db.session.add(new_user)

        try:
            db.session.commit()
            return {"message": f"Account for {username} successfully created!"}
        except IntegrityError:
            db.session.rollback()
            return cls.check_for_duplicate_acct(username, email)

    @classmethod
    def hash_pass(cls, pwd):
        """ Hash a new password """
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return hashed_utf8

    @classmethod
    def authenticate(cls, username, password):
        """ Ensure user exists. Check for correct password. Return boolean."""
        user = User.query.filter_by(username=username).first()

        return user and bcrypt.check_password_hash(user.password, password)

    @classmethod
    def check_for_duplicate_acct(cls, username, email):
        """ Check if account with username OR email exists """
        if User.query.filter_by(username=username).first() \
                or User.query.filter_by(email=email).first():
            return {"message": "Username/Email already taken!"}

    def __repr__(self):
        return '<User %r>' % self.username
