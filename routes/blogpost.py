""" Routes for blogpost-related tasks """
import flask_praetorian as fp
from flask import Blueprint, request, jsonify
from connect_models import db

blogpost_api = Blueprint('blogpost_api', __name__)


# BLOG POST ROUTE BY ID (GET)
# BLOG POSTS BY USER (GET)
# CREATE AND PATCH A BLOG POST (GET AND POST)
# EDIT A POST (PATCH)

