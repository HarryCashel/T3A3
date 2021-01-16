from main import ma
from models.Sub import Sub
from marshmallow.validate import Length
from schemas.PostSchema import posts_schema


class SubSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sub

    sub_name = ma.String(required=True, validate=Length(min=4))
    description = ma.String(required=True, validate=Length(min=4))
    posts = ma.Nested(posts_schema)

sub_schema = SubSchema()
subs_schema = SubSchema(many=True)
