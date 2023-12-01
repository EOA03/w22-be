import os
from db import db
from flask import Flask
from common.bcrypt import bcrypt
from auth.apis import auth_blueprint
from user.models import User
from flask_cors import CORS
from user.apis import user_blueprint
from todo.apis import todo_blueprint
from admin.apis import admin_blueprint

app = Flask(__name__)
CORS(app)

database_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

cors = CORS(app, resources={r"/api/*": {"origins": "https://localhost:3000"}})

@app.route("/")
def list_users():
  return "user example"

app.register_blueprint(auth_blueprint, url_prefix = "/auth")
app.register_blueprint(admin_blueprint, url_prefix = "/admin")
app.register_blueprint(user_blueprint, url_prefix = "/user", name="user_blueprint")
app.register_blueprint(todo_blueprint, url_prefix = "/todo")