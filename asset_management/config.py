import os
from flask import Flask
from dotenv import load_dotenv  
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# appilcation initialization
app = Flask("app")
db = SQLAlchemy()
migrate = Migrate(app, db)

# Conneting ,env file 
db_url = os.getenv('CONNECTION_URL')
app_secret_key = os.getenv("APP_SECRET_KEY")

app.secret_key = app_secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db.init_app(app)

loging_manager = LoginManager()
loging_manager.login_view = 'auth.login'
loging_manager.init_app(app)

@loging_manager.user_loader
def load_user(user_id):
    from sql_database.models import User
    return User.query.get(int(user_id))