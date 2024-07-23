from config import db
from uuid import uuid4
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    razorpay_customer_id = db.Column(db.String(255), nullable=True)
    subscription_id = db.Column(db.String(), nullable=True)
    groups = db.relationship('GroupName', backref='users', lazy=True)
    profile_id = db.relationship("Profile", uselist=False, backref="users", lazy=True)

    def __init__(self, name, email, password, razorpay_customer_id=None, is_admin=False, subscription_id=None):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.razorpay_customer_id = razorpay_customer_id
        self.is_admin = is_admin
        self.subscription_id = subscription_id

class GroupName(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    field = db.relationship('Field', backref='groups', lazy=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    status = db.relationship('Status', backref='groups', lazy=True)

    def __init__(self, name, description, user_id, created_date, updated_date):
        self.name = name
        self.user_id = user_id
        self.description = description
        self.created_date = created_date
        self.updated_date = updated_date

class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    field_key = db.Column(db.String(), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    dataformat_id = db.Column(db.Integer, db.ForeignKey('dataformats.id'), unique=False, nullable=False)
    required = db.Column(db.String())
    dataformat = db.relationship('DataFormat', back_populates='field')

    def __init__(self, name, description, dataformat_id, field_key, group_id, created_date, updated_date, required):
        self.name = name
        self.required = required 
        self.group_id = group_id
        self.field_key = field_key
        self.description = description
        self.created_date = created_date
        self.updated_date = updated_date
        self.dataformat_id = dataformat_id

class DataFormat(db.Model):
    __tablename__ = "dataformats"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    input_type = db. Column(db.String())
    field = db.relationship("Field", back_populates="dataformat", lazy='dynamic') 

    def __init__(self, name, input_type):
        self.name = name
        self.input_type = input_type
        
class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    mobile = db.Column(db.Integer)
    address = db.Column(db.String())
    position = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, name, email, mobile, address, position, user_id):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.address = address
        self.user_id = user_id
        self.position = position
    
class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    des = db.Column(db.String(), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, name, des, group_id, created_date, updated_date,):
        self.name = name
        self.group_id = group_id
        self.des = des
        self.created_date = created_date
        self.updated_date = updated_date         

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    subs_plan = db.relationship("Plan", backref="products", lazy=True)
    
    def __init__(self, name):
        self.name = name

class Plan(db.Model):
    __tablename__ = "plans"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    plan_id = db.Column(db.String(), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    def __init__(self, name, plan_id, product_id):
        self.name = name
        self.plan_id = plan_id
        self.product_id = product_id
