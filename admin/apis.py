from flask import Blueprint, request
from user.models import User
from todo.models import Todos
from admin.utils import admin_required
from db import db

admin_blueprint = Blueprint('user', __name__)

@admin_blueprint.route("", methods=["GET"])
@admin_required
def all_user_profile():
    users = User.query.all()
    
    user_profiles = [{
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role.value,
    } for user in users]

    return {"users": user_profiles}


@admin_blueprint.route("/<int:user_id>", methods=["GET"])
@admin_required
def users_profile(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404
    
    todos = Todos.query.filter_by(user_id=user_id).all()

    return {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role.value,
        "todos": todos
    }


@admin_blueprint.route("/todo", methods=["GET"])
@admin_required
def all_todo_list():
    todos = Todos.query.all()

    todo_list = []
    for todo in todos:
        user = User.query.get(todo.user_id)
        todo_list.append({
            "id": todo.id,
            "title": todo.title,
            "details": todo.details,
            "status": todo.status.value,
            "user_id": todo.user_id,
            "username": user.username
        })
    
    return {"todos": todo_list}, 200


@admin_blueprint.route("/todo/<int:user_id>", methods=["GET"])
@admin_required
def all_todo_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    todos = Todos.query.filter_by(user_id=user_id).all()

    todo_list = [{
        "id": todo.id,
        "title": todo.title,
        "details": todo.details,
        "status": todo.status.value,
        "user_id": todo.user_id,
        "username": user.username
    } for todo in todos]

    return {"data":todo_list}, 200


@admin_blueprint.route("/todo/<int:id>", methods=["DELETE"])
@admin_required
def delete_todo(id):
    todo = Todos.query.get(id=id)

    if not todo:
        return {"error": "Todo not found"}, 404

    db.session.delete(todo)
    db.session.commit()

    return {"message": "Seccessfully delete a todo"}, 200
