import os
import datetime
from flask import jsonify
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('faith.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    name = CharField()
    email = CharField(unique=True)
    password = CharField(max_length=100)
    class Meta:
        database = DATABASE
        db_table = 'user'

    @classmethod
    def create_user(cls, username, name, email, password):
        try:
            cls.create(
                username = username,
                name = name,
                email = email,
                password = generate_password_hash(password))
        except IntegrityError:
            raise ValueError("create error")

    @classmethod
    def edit_user(cls, username, email, password, location):
        try:
            cls.create(
                username = username,
                email = email,
                name = name,
                password = generate_password_hash(password))
        except IntegrityError:
            raise ValueError("create error")

class Post(Model):
    title = CharField(max_length=100)
    category = CharField(max_length = 30)
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now())
    user = ForeignKeyField(User, backref="posts")

    class Meta:
        database = DATABASE
        db_table = 'post'
        order_by = ('+timestamp',)

    @classmethod
    def create_post(cls, title, category, content, user):
        try:
            cls.create(
                title = title,
                category = category,
                content = content,
                user = user)
        except IntegrityError:
            raise ValueError("Create Post Error! Oh no!")
            
class Reply(Model):
    user = ForeignKeyField(User, backref="user")
    post = ForeignKeyField(Post, backref="posts")
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now())
    class Meta:
        database = DATABASE
        db_table = 'reply'
        order_by = ('+timestamp',)

class ReplyThread(Model):
    user = ForeignKeyField(User, backref="replies")
    reply = ForeignKeyField(Reply, backref="comments")
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE
        db_table = 'reply_thread'
        order_by = ('+timestamp',)

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Reply, ReplyThread], safe=True)
    DATABASE.close()