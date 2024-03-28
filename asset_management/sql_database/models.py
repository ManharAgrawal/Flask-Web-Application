from uuid import uuid4
from config import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    groups = db.relationship('GroupName', backref='users', lazy=True)

    def __init__(self, name, email, password): 
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

class GroupName(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    field = db.relationship('Field', backref='groups', lazy=True)

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id

class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    dataformat = db.Column(db.String(), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    field_key = db.Column(db.String(), nullable=False)

    def __init__(self,name,description, dataformat, field_key, group_id):
        self.name = name
        self.description = description
        self.dataformat = dataformat
        self.group_id = group_id
        self.field_key = field_key