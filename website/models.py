from flask import Blueprint
from flask_login import UserMixin
from . import db

models = Blueprint('models', __name__)


# class Password:
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complete_count = db.Column(db.Integer, default=0)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    status = db.Column(db.String(20))
    created_on = db.Column(db.String(20))
    tasks = db.relationship('Task', backref='project', lazy=True)

    def __init__(self, user_id, title, content, status, tasks=[]):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.status = status

    def add_tasks(self, task):
        self.tasks.append(task)

    # def update_status(self):
    #     self.complete_count = 0
    #     for task in self.tasks:
    #         if task.status == "Complete":
    #             self.complete_count += 1
    #     if len(self.tasks) == 0:
    #         self.status = "Open"
    #     elif len(self.tasks) == 100:
    #         self.status = "Complete"
    #     else:
    #         self.status = str(int((self.complete_count / len(self.tasks)) * 100)) + "%"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    status = db.Column(db.String(20))
    created_on = db.Column(db.String(20))
    updated_on = db.Column(db.String(20))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.String(20))
    updated_on = db.Column(db.String(20))
    projects = db.relationship('Project', backref='user', lazy=True)
