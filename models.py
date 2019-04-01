import os
from flask import jsonify
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime
from peewee import *


# Sets DATABASE variable for development
DATABASE = SqliteDatabase('faith.db')

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([], safe=True)
    DATABASE.close()
