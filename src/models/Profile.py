from main import db
from models.Sub import Sub
from models.Post import Post
from models.Comment import Comment

class Profile(db.Model):
    """Model to represent a user's profile"""
    __tablename__ = "profiles"

    profile_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    about = db.Column(db.String(), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id"), nullable=False
    )
    subs = db.relationship(
        "Sub", backref="profile", lazy="dynamic", cascade="all, delete, delete-orphan"
    )
    posts = db.relationship(
        "Post", backref="profile", lazy="dynamic", cascade="all, delete, delete-orphan"
    )
    comments = db.relationship(
        "Comment", backref="profile", lazy="dynamic", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"<Profile (id='{self.id}', username='{self.username}')>"