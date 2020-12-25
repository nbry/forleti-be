from flask_praetorian import Praetorian
from flask_sqlalchemy import SQLAlchemy

guard = Praetorian()
db = SQLAlchemy()


def connect_db(app, user):
    """
    Initialize Praetorian with app.
    Connect database to provided Flask app.
    """
    guard.app = app
    guard.init_app(app, user)
    db.app = app
    db.init_app(app)
