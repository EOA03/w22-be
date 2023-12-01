from db import db
from enum import Enum

class StatusTodo(Enum):
    notStarted = 'not started'
    inProgress = 'in progress'
    done = 'done'

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(200), nullable = False)
    status = db.Column(db.Enum(StatusTodo), nullable=False, default=StatusTodo.notStarted)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    user = db.relationship('User', backref = db.backref('todo', lazy = True))