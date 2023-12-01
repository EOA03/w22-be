from flask import Blueprint, request
from common.bcrypt import bcrypt
from user.models import User, UserRole
from db import db
import jwt, os
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError

auth_blueprint = Blueprint("auth", __name__)

class EnumField(fields.Field):
    def __init__(self, enum, *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        self.enum = enum

    def _serialize(self, value, attr, obj, **kwargs):
        return value.value

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None

        try:
            return self.enum(value.lower())
        except ValueError:
            raise ValidationError(f'Invalid enum value for {attr}. Allowed values are: {", ".join(member.value for member in self.enum)}')

class UserRegistrationSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role = EnumField(UserRole, required=True)

    def get_role_default(self):
        return UserRole.user

@auth_blueprint.route("/registration", methods=["POST"])
def register():
    data = request.get_json()
    schema = UserRegistrationSchema()

    try:
        data = schema.load(data, unknown="raise")
    except ValidationError as err:
        return {"error": err.messages}, 400
    
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return{'error': "Username already exist"}, 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password, role=data['role'].value)
    db.session.add(new_user)
    db.session.commit()

    return {
        'message': "User successfully registered"
    }

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"error": "username or password is incorrect"}, 400
    
    valid_password = bcrypt.check_password_hash(user.password, password)
    if not valid_password:
        return {"error": "username or password is incorrect"}, 400
    
    payload = {
        'user_id': user.user_id,
        'username': user.username,
        'role': user.role.value,
        'exp': datetime.utcnow() + timedelta(minutes=10)
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
    
    return {
        'token': token
    }