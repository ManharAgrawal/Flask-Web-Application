import os
from flask import Flask
from dotenv import load_dotenv  
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_mail import Mail

load_dotenv()

app = Flask("app")

# Connecting SQLAlchemy for the database (PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CONNECTION_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_secret_key = os.getenv("APP_SECRET_KEY")
app.secret_key = app_secret_key

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Connecting SQLAlchemy for the database2 (MongoDB)
mongo_url = os.getenv('MONGO_URL')
app.config['MONGO_URI'] = os.getenv('MONGO_URL')
app.config['SQLALCHEMY_BINDS'] = {'mongo': mongo_url}
mongo = PyMongo(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from sql_database.models import User
    return User.query.get(int(user_id))

# Email validation

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = 'manharagrawal19@gmail.com'
app.config["MAIL_PASSWORD"] = 'qjhyxshwlchkocwk'
app.config["MAIL_USE_TLS"] = True # Transport Layer Security 
app.config["MAIL_USE_SSL"] = False # Secure Socket Layer

mail = Mail(app)