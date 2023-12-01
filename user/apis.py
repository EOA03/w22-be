from flask import Blueprint, request
from user.models import User
from auth.utils import decode_jwt
from todo.models import Todos

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route("", methods=["GET"])
def user_profile():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return {"error": "Invalid token format"}, 401

    token = auth_header.split(' ')[1]

    try:
        payload = decode_jwt(token)
    except Exception as e:
        print(f"Error decoding token: {e}")
        return {"error": "Token is invalid"}, 401

    if not payload or "user_id" not in payload:
        return {"error": "Token is invalid"}, 401

    user = User.query.get(payload["user_id"])

    if not user:
        return {"error": "User not found"}, 404
    
    todos = Todos.query.filter_by(user_id = payload['user_id']).all()

    return {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role.value,
        "todos": [{
            "id": todo.id,
            "title": todo.title,
            "details": todo.details,
            "status": todo.status.value
        } for todo in todos]
    }
