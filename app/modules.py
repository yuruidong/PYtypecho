# coding: utf-8
import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager

Permission = ('admin', 'writer', 'normal')


class User(UserMixin, db.Document):
    """
    用户文档集
    """
    email = db.EmailField(required=True, unique=True)
    username = db.StringField(max_length=20, required=True, unique=True)
    password_hash = db.StringField(max_length=128, required=True)
    user_type = db.StringField(choices=Permission, default='normal')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def user_load(user_id):
    return User.objects(id=user_id).first()


class Comment(db.EmbeddedDocument):
    """
    评论文档集
    """
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)


class Post(db.DynamicDocument):
    """
    文章文档集
    """
    create_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    tags = db.ListField(db.StringField())
    content = db.StringField()
    comment = db.ListField(db.EmbeddedDocumentField("Comment"))

