from flask import Blueprint
from flask_login import UserMixin
from . import db

models = Blueprint('models', __name__)


class Password:
    def __init__(self, id, password):
        self.id = id
        self.password = password


class Project():
    def __init__(self, id, title, content, created_on):
        self.id = id
        self.title = title
        self.content = content
        self.complete_count = 0
        self.created_on = created_on
        self.updated_on = None
        self.status = 0
        self.tasks = []

    def add_tasks(self, tasks):
        self.tasks.append(tasks)

    def update_status(self):
        for task in self.tasks:
            if task.status == "Complete":
                self.complete_count += 1
        self.status = (self.complete_count / len(self.tasks)) * 100


class Tasks():
    def __init__(self, id, project_id, title, content, status, created_on, updated_on):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.content = content
        self.status = status
        self.created_on = created_on
        self.updated_on = updated_on


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    created_on = db.Column(db.String(20), nullable=False)
    updated_on = db.Column(db.String(20), nullable=False)
