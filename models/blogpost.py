from connect_models import db


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
