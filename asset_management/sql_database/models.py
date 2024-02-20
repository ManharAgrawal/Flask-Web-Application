from uuid import uuid4
from flask import request
from config import app , db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    is_active = db.Column(db.Boolean)
    groups = db.relationship('GroupName', backref='user', secondary='users_groups')

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
    
    def __init__(self, name, description):
        self.name = name
        self.description = description

# Association Table For Relationship
users_groups = db.Table(
    'users_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.PrimaryKeyConstraint('user_id', 'group_id')
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())

    def __repr__(self):
        return f'<Tag "{self.name}">' 

class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String)
    comments = db.relationship('GroupsName', backref='Relation')
    tags = db.relationship('Tag', secondary=users_groups, backref='Relation')

    def __repr__(self):
        return f'<Post "{self.title}">'
    
    
""" 
    ====================================================
                
                User Email & Pass

1. userone@gmail.com - 1234 (created)
2. mario@gmail.com - 5678
3. slugterra@gmail.com - 0000
4. superman@gmail.com - 1111
5. chip&dale@gmail.com - 5555
6. snowbros@gmail.com - 1010
7. bowser@gmail.com - 2222
8. tom@gmail.com - 4040
9. deadpool@gmail.com - 6666
10. whoami@gmail.com - 5050 (created)

    ===========================================================
"""
