""" Routes for blogpost-related tasks """
import flask_praetorian as fp
from flask import Blueprint, request, jsonify
from connect_models import db

blogpost_api = Blueprint('blogpost_api', __name__)


# BLOG POST ROUTE BY ID (GET)
# BLOG POSTS BY USER (GET)
# CREATE AND PATCH A BLOG POST (GET AND POST)
# EDIT A POST (PATCH)

class BlogPost(db.Model):
    __tablename__ = "blogposts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False)

    user = db.relationship("User")
