""" Seed file to make sample data for db. """

from project.extensions import db

# MUST import app for seeding to work
# noinspection PyUnresolvedReferences
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

print("Tables Created!")
