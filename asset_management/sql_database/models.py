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
    is_active = db.Column(db.Boolean)
    groups = db.relationship('GroupName', backref='users', lazy=True)
    
    def __init__(self, name, email, password, is_active=True): 
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_active = is_active
        
class GroupName(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    field = db.relationship('Field', backref='GroupName', lazy=True)

    def __init__(self, name, description, user):
        self.name = name
        self.description = description
        self.user = user

class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
    default = db.Column(db.String(), nullable=False)
    group_name_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    
    def __init__(self,name,text,default,group_name_id):
        self.name = name
        self.text = text
        self.default = default
        self.group_name_id = group_name_id