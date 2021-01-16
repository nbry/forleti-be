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
            "content": new_blogpost.content
        }
        return jsonify({"blogpost": blogpost})
    else:
        message = {
            "status": 401,
            "message": "Blog post not created. Something went wrong"}
        return jsonify(message)

#     TO BE FINISHED AFTER FRONT END WYSIWYG EDITOR IS CONFIGURED...
