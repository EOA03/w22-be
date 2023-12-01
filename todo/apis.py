from flask import Blueprint, request
from todo.models import Todos
from auth.utils import decode_jwt
from db import db
from marshmallow import Schema, fields, ValidationError
from admin.utils import admin_required

todo_blueprint = Blueprint('todo', __name__)

class CreateTodoSchema(Schema):
    title = fields.String(required=True)
    details = fields.String(required=True)


@todo_blueprint.route("", methods=["POST"])
def create_todo():
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
    
    if not request.is_json:
        return {"error": "Not JSON"}, 400
    
    data = request.get_json()
    schema = CreateTodoSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error": err.messages}, 400
    
    todos = Todos(title=data['title'], details=data['details'], user_id=payload['user_id'])

    db.session.add(todos)
    try:
        db.session.commit()
        return {"message": "Successfully create a todo list"}, 200
    except Exception as e:
        print(f"Error committing to the database: {e}")
        db.session.rollback()
        return {"error": "Failed to create a todo list"}, 500
    finally:
        db.session.close()


@todo_blueprint.route("/<int:id>", methods=["PATCH"])
def update_status(id):
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

    todo = Todos.query.get(id)

    if not todo:
        return {"error": "Todo not found"}, 404

    if todo.user_id != payload['user_id']:
        return {"error": "Unauthorized to delete this todo"}, 403

    data = request.get_json()

    if 'status' in data:
        todo.status = data['status']
    
    db.session.commit()

    return {
        "message": "Successfully update status",
        "todo": todo.to_dict()
    }, 200


@todo_blueprint.route("/<int:id>", methods=["PUT"])
def update_todo(id):
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

    todo = Todos.query.get(id)

    if not todo:
        return {"error": "Todo not found"}, 404

    if todo.user_id != payload['user_id']:
        return {"error": "Unauthorized to delete this todo"}, 403

    data = request.get_json()

    if 'title' in data:
        todo.title = data['title']
    
    if 'details' in data:
        todo.details = data['details']
    
    db.session.commit()

    return {
        "message": "Successfully update a todo",
        "todo": {
            "id": todo.id,
            "title": todo.title,
            "details": todo.details,
            "status": todo.status.value,
            "user_id": todo.user_id
        }
    },200


@todo_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_todo(id):
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

    todo = Todos.query.get(id)

    if not todo:
        return {"error": "Todo not found"}, 404

    if todo.user_id != payload['user_id']:
        return {"error": "Unauthorized to delete this todo"}, 403
    
    db.session.delete(todo)
    db.session.commit()

    return {"message": "Successfully delete a todo list"}, 200
