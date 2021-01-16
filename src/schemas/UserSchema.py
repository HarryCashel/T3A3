from flask_sqlalchemy import model
from marshmallow import validate
from main import ma
from models.User import User
from marshmallow.validate import Length


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]

    full_name = ma.String(required=True, validate=Length(min=3))
    email = ma.String(required=True, validate=Length(min=6))
    password = ma.String(required=True, validate=Length(min=6))

user_schema = UserSchema()
users_schema = UserSchema(many=True)