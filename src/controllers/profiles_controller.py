import flask_jwt_extended
from models.User import User
from models.Profile import Profile
from schemas.ProfileSchema import profile_schema, profiles_schema
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from main import db

profiles = Blueprint("profiles", __name__, url_prefix="/profiles")


@profiles.route("/", methods=["GET"])
@jwt_required
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="No user found")
    
    profile = Profile.query.filter_by(user_id=user.user_id)

    return jsonify(profile_schema.dump(profile))


@profiles.route("/<int:id>", methods=["GET"])
@jwt_required
def get_profile_by_id(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="No user found")

    profile = Profile.query.filter_by(profile_id=id, user_id=user.user_id)

    if profile.count() != 1:
        return abort(404, description="No profile found")

    return jsonify(profile_schema.dump(profile[0]))


@profiles.route("/create", methods=["POST"])
@jwt_required
def create_profile():
    profile_fields = profile_schema.load(request.json)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="No user found")

    new_profile = Profile()
    new_profile.username = profile_fields["username"]
    new_profile.about = profile_fields["about"]
    
    user.profiles.append(new_profile)
    db.session.commit()

    return jsonify(profile_schema.dump(new_profile))


@profiles.route("/<int:id>", methods=["PATCH"])
@jwt_required
def update_profile():
    profile_fields = profile_schema.load(request.json, partial=True)
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return abort(401, description="No user found")

    profile = Profile.query.filter_by(profile_id=id, user_id=user.user_id)

    if profile.count() != 1:
        return abort(401, description="No profile found for your user")

    profile.update(profile_fields)
    db.session.commit()

    return jsonify(profile_schema.dump(profile[0]))


@profiles.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_profile():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return abort(401, description="No user found")

    profile = Profile.query.filter_by(profile_id=id, user_id=user.user_id).first()

    if profile.count() != 1:
        return abort(401, description="No profile found for your user")

    db.session.delete(profile)
    db.session.commit()

    return jsonify(profile_schema.dump(profile))

