from flask import Blueprint
from flask_login import UserMixin
from sqlalchemy import func
from . import db

models = Blueprint('models', __name__)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    status = db.Column(db.String(255))
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    # tasks = db.relationship('Task', backref='project', lazy=True)

    def __init__(self, user_id, title, content, status):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.status = status


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    status = db.Column(db.String(255))
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    # projects = db.relationship('Project', backref='user', lazy=True)
