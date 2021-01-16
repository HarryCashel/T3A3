from main import ma
from models.Post import Post
from marshmallow.validate import Length
from schemas.CommentSchema import comments_schema


class PostSchema(ma.SQLAlchemyAutoSchema):
    class meta:
        model = Post
    
    post_name = ma.String(required=True, validate=Length(min=1))
    post = ma.String(required=True, validate=Length(min=1))
    comments = ma.Nested(comments_schema)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)