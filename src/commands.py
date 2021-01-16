from types import new_class
from main import db
from flask import Blueprint

db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables deleted!")

@db_commands.cli.command("seed")
def seed_db():
    from models.User import User
    from models.Profile import Profile
    from models.Sub import Sub
    from models.Post import Post
    from models.Comment import Comment
    from main import bcrypt
    import random
    from faker import Faker

    faker = Faker()
    users = []
    profiles = []
    subs = []
    comments = []
    posts = []
    profile_ids = list(range(1,6))
    random.shuffle(profile_ids)
    post_ids = list(1,11)
    random.shuffle(post_ids)

    for i in range(5):
        user = User()
        user.full_name = faker.name()
        user.email = f"fake_emaiil{i}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    print("User table seeded")

    for i in range(5):
        profile = Profile()
        profile.username = faker.name()
        profile.about = faker.sentence()
        profile.user_id = random.choice(users).user_id
        db.session.add(profile)
        profiles.append(profile)
    
    db.session.commit()
    print("Profile table seeded")
        
    for i in range(10):
        sub = Sub()
        sub.sub_name = faker.name()
        sub.description = faker.sentence()
        sub.profile_id = random.choice(profiles)
        db.session.add(sub)
        subs.append(sub)

    db.session.commit()
    print("Subs table seeded")

    for i in range(10):
        new_post = Post()
        new_post.post_name = faker.name()
        new_post.post = faker.text()
        new_post.profile_id = random.choice(profiles)
        db.session.add(new_post)
        posts.append(new_post)

    db.session.commit()
    print("Posts table seeded")

    for i in range(10):
        new_comment = Comment()
        new_comment.comment = faker.text()
        new_comment.post_id = random.choice(post_ids)
        db.session.add(new_comment)
    
    db.session.commit()
    print("Comments table seeded")



