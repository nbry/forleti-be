from flask_praetorian import Praetorian
from flask_sqlalchemy import SQLAlchemy

# Create globally accessible instances of Flask extensions.
db = SQLAlchemy()
guard = Praetorian()