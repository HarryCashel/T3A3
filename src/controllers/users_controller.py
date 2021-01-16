import jwt
from models.User import User
from models.Profile import Profile
from schemas.UserSchema import UserSchema, user_schema
from main import db
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta

users = Blueprint("users", __name__, url_prefix="/users")

@users.route("/", methods=["GET"])
@jwt_required
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="No user found")
    
    return jsonify(user_schema.dump(user))


@users.route("/register", methods=["POST"])
def user_register():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"].first())

    if user:
        return abort(401, description="Email already in use")
    
    user = User()
    user.full_name = user_fields["full_name"]
    user.email = user_fields["email"]
    user.create_password(user_fields["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@users.route("/login", methods=["POST"])
def user_login():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not user.check_password(user_fields["password"]):
        return abort(401, description="Invalid email and password")
    
    expiry = timedelta(days=1)
    access_token = create_access_token(
        identity=str(user.user_id), expires_delta=expiry
    )

    return jsonify({"token": access_token})

@users.route("/", methods=["PATCH"])
@jwt_required
def update_user():
    user_id = get_jwt_identity()

    user = User.query.filter_by(user_id=user_id)

    if not user:
        return abort(401, description="No user found")
    
    update_fields = user_schema.load(request.json, partial=True)
    user.update(update_fields)
    db.session.commit()
    return jsonify(user_schema.dump(user[0]))

@users.route("/", methods=["DELETE"])
@jwt_required
def delete_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(404, description="No user found")

    db.session.delete(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


