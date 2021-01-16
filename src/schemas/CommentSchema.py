from main import ma
from main import ma
import marshmallow.validate
from models.Comment import Comment
from marshmallow.validate import Length


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
    
    comment = ma.String(required=True, validate=Length(min=1))

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)