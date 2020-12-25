from flask_praetorian import Praetorian
from flask_sqlalchemy import SQLAlchemy
from models.user import User

# Initializing Flask Praetorian base module
guard = Praetorian()

# Initilizing Flask SQLAlchemy base module
db = SQLAlchemy()


def connect_db(app):
    """
    Connect Flask Praetorian to app.
    Connect database to provided Flask app.
    """
    guard.init_app(app, User)
    db.app = app
    db.init_app(app)
