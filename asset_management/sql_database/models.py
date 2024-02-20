from werkzeug.security import generate_password_hash
from uuid import uuid4
from config import app , db
from flask import request
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    is_active = db.Column(db.Boolean)

    def __init__(self, name, email, password,is_active=True):  
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_active = is_active
        
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.String(), primary_key=True) 
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    contact = db.Column(db.Integer(), nullable=False)
    salary = db.Column(db.Integer(), nullable=False)
    department = db.Column(db.String(), nullable=False)
    
    def __init__(self,name,email,contact,salary,department):
        self.name = name
        self.email = email
        self.contact = contact
        self.salary = salary
        self.department = department