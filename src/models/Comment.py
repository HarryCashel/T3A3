from main import db


class Comment(db.Model):
    """Model to represent comments on posts"""
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("profile.profile_id", nullable=False)
    )
    post_id = db.Column(
        db.Integer, db.ForeignKey("post.post_id", nullable=False)
    )

    def __repr__(self):
        return f"<Comment {self.comment_id}>"