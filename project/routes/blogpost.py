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
            "content": res.content,
            "created": res.created,
            "author": res.user
        }
        return jsonify({"blogpost": blogpost})
    else:
        message = {"message": f"No blog post with id {blogpost_id} found"}
        return jsonify(message)


@blogpost_api_blueprint.route('/bp/new', methods=["POST"])
@fp.auth_required
def create_new_blog_post():
    """
    Create a new blog post
    """
    req = request.json

    user_id = fp.current_user_id()
    title = req.get("title", None)
    content = req.get("content", None)

    new_blogpost = BlogPost.create_new_blogpost(user_id, content, title)

    if new_blogpost:
        blogpost = {
            "title": new_blogpost.title,
            "content": new_blogpost.content,
            "created": new_blogpost.created,
            "author": fp.current_user().username
        }
        return jsonify({"blogpost": blogpost})
    else:
        message = {
            "status": 401,
            "message": "Blog post not created. Something went wrong"}
        return jsonify(message)


@blogpost_api_blueprint.route('/bp/<int:blogpost_id>/edit', methods=["PATCH"])
@fp.auth_required
def edit_blog_post(blogpost_id):
    """
    Check if logged in user matches the author of the blogpost.
    If so, update blogpost with new content.
    """
    blogpost = BlogPost.find_blogpost_by_id(blogpost_id)

    if blogpost.user_id != fp.current_user_id():
        return jsonify({"message": "Unauthorized"}), 401

    req = request.json

    message = BlogPost.update_blogpost(
        blogpost_id,
        title=req.title,
        content=req.content)

    return message


@blogpost_api_blueprint.route('/bp/<int:blogpost_id>/delete', methods=["DELETE"])
@fp.auth_required
def delete_blog_post(blogpost_id):
    """
    Check if logged in user matches the author of the blogpost.
    If so, delete the blogpost.
    """
    blogpost = BlogPost.find_blogpost_by_id(blogpost_id)

    if blogpost.user_id != fp.current_user_id():
        return jsonify({"message": "Unauthorized"}), 401

    message = BlogPost.delete_blogpost(blogpost_id)

    return message
