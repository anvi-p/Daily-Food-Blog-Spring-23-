from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    def get_id(self):
        return self.username

class Post(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=1000)
    date = db.StringField(required=True)
    post_id = db.IntField(required=True, min_length=5, max_length=5)
    post_title = db.StringField(required=True, min_length=1, max_length=100)
    meal_type = db.StringField(requied=True)
    home_rest = db.StringField(required=True)
    image = db.ImageField()

class Comment(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    post_id = db.IntField(required=True, min_length=5, max_length=5)