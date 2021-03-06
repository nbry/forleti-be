from datetime import datetime
from flask import jsonify
from project.extensions import db


class BlogPost(db.Model):
    __tablename__ = "blogposts"

    # [UTILITY] Provide a getter method. In other words, allow attributes to
    # be retrieved with square bracket notation.
    # e.g. getting a blog's title --> blogpost.title OR blogpost['title']
    #
    # NOTE: you still can't assign a new value using bracket notation.
    # For example, if you wanted to change a post's title to 'New Recipe',
    # blogpost['title'] = 'New Recipe' still won't work. To do this, access the
    # use setattr method (i.e. setattr(blogpost, 'title', 'New Recipe')
    def __getitem__(self, key):
        return self.__dict__[key]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    edited = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # *****************************
    # CRUD methods:
    # *****************************

    @classmethod
    def find_blogpost_by_id(cls, blogpost_id: int):
        """
        Search database for blog post by id. Return blog post or 404 error.
        """
        return cls.query.get_or_404(blogpost_id)

    @classmethod
    def create_new_blogpost(cls, user_id, content, title):
        """
        Create a new blog post. Return blogpost
        """
        new_blogpost = cls(user_id=user_id, content=content, title=title)
        db.session.add(new_blogpost)

        # noinspection PyBroadException
        try:
            db.session.commit()
            return new_blogpost

        except Exception:
            db.session.rollback()
            return None

    @classmethod
    def delete_blogpost(cls, blogpost_id: int):
        """
        Identify blog post by id. Delete if matching post is found.
        """
        blogpost = cls.find_blogpost_by_id(blogpost_id)

        if blogpost:
            # noinspection PyBroadException
            try:
                db.session.delete(blogpost)
                db.session.commit()
                return jsonify({"message": "Post deleted!"}), 200
            except Exception:
                db.session.rollback()
                return jsonify({"message": "Something went wrong."}), 200
        else:
            return jsonify({"message": f"No post with id {blogpost_id} found"})

    @classmethod
    def update_blogpost(cls, blogpost_id, **kwargs):
        """
        Find a post by id. Looks for "title" or "content" within
        kwargs and updates the blog post with the provided items.

        e.g.
        update_blogpost(3, title="New Dog", age=9)
        -> Finds blogpost with id of 3
        -> Updates title to "New Dog"
        -> age parameter is ignored.
        -> Sets "edited" to True
        """

        blogpost = cls.find_blogpost_by_id(blogpost_id)
        blogpost.title = kwargs.get("title", blogpost.title)
        blogpost.content = kwargs.get("content", blogpost.content)
        blogpost.edited = True

        # noinspection PyBroadException
        try:
            db.session.commit()
            return jsonify({"message": "Post updated!"}), 200
        except Exception:
            db.session.rollback()
            return jsonify({"message": "Something went wrong."}), 400
