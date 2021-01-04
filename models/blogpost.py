from connect_models import db


class BlogPost(db.model):
    __tablename__ = "blogposts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
