from main import ma
from models.Comment import Comment
from models.Sub import Sub
from models.User import User
from models.Profile import Profile
from models.Post import Post
from schemas.SubsSchema import sub_schema, subs_schema
from schemas.ProfileSchema import profile_schema, profiles_schema
from schemas.PostSchema import post_schema
from main import db
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from sqlalchemy.orm import joinedload
from src.schemas.CommentSchema import comment_schema

subs = Blueprint("subs", __name__, url_prefix="/subs")


def retrieve_profile(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="No user found")

    profile = Profile.query.filter_by(
        profile_id=id, user_id=user.user_id).first()

    if not profile:
        return abort(404, description="No profile found")

    return profile


@subs.route("/", methods=["GET"])
def show_subs():
    # Show all subs
    subs = Sub.query.options(joinedload("profile")).all()
    return jsonify(subs_schema.dump(subs))


@subs.route("/<int:id>", methods=["GET"])
def sub_show(id):
    # Show specific sub's posts
    sub = Sub.query.filter_by(sub_id=id).first()

    if not sub:
        return abort(404, description="Sub not found")

    posts = Post.query.filter_by(sub_id=sub.sub_id)
    
    return jsonify(sub_schema.dump(posts))


@subs.route("/", methods=["POST"])
def create_sub():
    # creates a sub
    profile = retrieve_profile(request.args["profile_id"])

    sub_fields = sub_schema.load(request.json)
    new_sub = Sub()
    new_sub.sub_name = sub_fields["sub_name"]
    new_sub.description = sub_fields["description"]
    new_sub.profile_id = sub_fields["profile_id"]

    db.session.add(new_sub)
    db.session.commit()


@subs.route("/<int:id>", methods=["DELETE"])
def delete_sub(id):
    # deletes a sub
    profile = retrieve_profile(request.args["profile_id"])

    sub_search = Sub.query.filter_by(sub_id=id).first()

    if not sub_search:
        return abort(404, description="Sub not found")
    
    db.session.delete(sub_search)
    db.session.commit()

    return jsonify(sub_schema.dump(sub_search))


@subs.route("/<int:id>/post", methods=["POST"])
def create_post(id):
    # creates a post in a specific sub
    profile = retrieve_profile(request.args["profile_id"])

    sub_search = Sub.query.filter_by(sub_id=id).first()

    if not sub_search:
        return abort(404, description="Sub not found")
    
    post_fields = post_schema.load(request.json)
    new_post = Post()
    new_post.post_name = post_fields["post_name"]
    new_post.post = post_fields["post"]
    
    db.session.add(new_post)
    db.session.commit()

    return jsonify(post_schema.dump(new_post))


@subs.route("/<int:id>/post/", methods=["DELETE"])
def delete_post(id):
    # deletes a post in a specific sub
    profile = retrieve_profile(request.args["profile_id"])

    sub_search = Sub.query.filter_by(sub_id=id).first()

    if not sub_search:
        return abort(404, description="Sub not found")
    
    post = post_schema.load(request.json, partial=True)

    for item in sub_search.posts:
        if item.post_id == post["post_id"]:
            sub_search.post.remove(item)
            db.session.commit()
            return jsonify(sub_schema.dump(sub_search))
    
    return abort(404, description="Post not found")


@subs.route("/<int:id>/post/<string:name>", methods=["GET"])
def get_post(id, name):
    # retrieves a specific post
    pass

    
@subs.route("/<int:id>/post/<string:name>/comment")
def create_comment(id, name):
    # creates a comment on a specific post
    sub_search = Sub.query.filter_by(sub_id=id).first()

    if not sub_search:
        return abort(404, description="Sub not found")
    
    post_search = Post.query.filter_by(post_name=name).first()

    if not post_search:
        return abort(404, description="Post not found")
    
    comment_field = comment_schema.load(request.json)
    new_comment = Comment()
    new_comment.comment = comment_field["comment"]

    db.session.add(new_comment)
    db.session.commit()

    return jsonify(comment_schema(new_comment))

