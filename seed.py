""" Seed file to make sample data for db. """

from models import db

# Create all tables
db.drop_all()
db.create_all()
