""" Seed file to make sample data for db. """

from project import db

# MUST import app for seeding to work
# noinspection PyUnresolvedReferences
from app import app

# Create all tables
db.drop_all()
db.create_all()

print("Tables Created!")
