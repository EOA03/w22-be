from db import db
from enum import Enum

class UserRole(Enum):
    admin = 'admin'
    user = 'user'

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    role = db.Column(db.Enum(UserRole), nullable = False)