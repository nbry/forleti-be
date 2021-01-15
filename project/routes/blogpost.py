""" Routes for blogpost-related tasks """
import flask_praetorian as fp
from flask import jsonify, request
from project.models import BlogPost, User
from . import blogpost_api_blueprint


@blogpost_api_blueprint.route('/bp/<int:blogpost_id>')
def get_blogpost_by_id(blogpost_id):
    """
    Search for a blog post based on id.
    If matching blog post found, return post.
    """
    res = BlogPost.query.get(blogpost_id)

    if res:
        blogpost = {
            "title": res.title,
            "subtitle": res.subtitle,
            "content": res.content,
            "author": res.user
        }
        return jsonify({"blogpost": blogpost})
    else:
        message = {"message": f"No blog post with id {blogpost_id} found"}
        return jsonify(message)


@blogpost_api_blueprint.route('/bp/new')
@fp.auth_required
def create_new_blog_post():
    """
    Create a new blog post
    """
    req = request.json


#     TO BE FINISHED AFTER FRONT END WYSIWYG EDITOR IS CONFIGURED...


@blogpost_api_blueprint.route('/<username>')
def get_blogposts_by_username(username):
    """
    Search for a user by username.
    If matching user is found, return all blog posts made by the user.
    Supply relevant information to load a "profile page". i.e. return the
    user's username and bio as well.
    """
    res = User.lookup(username)
    if res:
        user = {
            "posts": res.posts,
            "username": res.username,
            "bio": res.bio,
        }
        return jsonify({"user": user})

    # BLOG POSTS BY USER (GET)
    # CREATE AND PATCH A BLOG POST (GET AND POST)
    # EDIT A POST (PATCH)
