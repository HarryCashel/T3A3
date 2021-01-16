from main import ma
from marshmallow.validate import Length
import marshmallow.validate
from models.Profile import Profile
from schemas.UserSchema import UserSchema
from schemas.SubsSchema import subs_schema
from schemas.PostSchema import posts_schema
from schemas.CommentSchema import comments_schema
from models.Comment import Comment



class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class meta:
        model = Profile

    username = ma.String(required=True, validate=Length(min=2))
    about = ma.String(required=True, validate=Length(min=4))
    user = ma.Nested(UserSchema)
    subs = ma.Nested(subs_schema)
    posts = ma.Nested(posts_schema)
    comments = ma.Nested(comments_schema)

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
