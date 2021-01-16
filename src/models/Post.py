from main import db


class Post(db.Model):
    """Model to represent the posts on sub-sections"""
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(), nullable=False)
    post = db.Column(db.Text, nullable=False)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("profile.profile_id", nullable=False)
    )
    sub_id = db.Column(
        db.Integer, db.ForeignKey("sub.sub_id", nullable=False)
    )
    comments = db.relationship(
        "Comment", backref="profile", lazy="dynamic", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"<Post {self.post_id}>"