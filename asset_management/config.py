import os
from flask import Flask
from dotenv import load_dotenv  
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from pymongo import MongoClient 

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