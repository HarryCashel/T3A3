from sqlalchemy.orm import backref
from main import db
from models.Profile import Profile
from models.Post import Post


class Sub(db.model):
    """Model to represent a sub-section of the website"""
    __tablename__ = "subs"

    sub_id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text, nullable=False)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("profile.profile_id", nullable=False)
    )
    posts = db.relationship(
        "Post", backref="subs", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Subs {self.sub_id}>"