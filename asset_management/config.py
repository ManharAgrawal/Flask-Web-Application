import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from sql_database.models import db, Comment, Tag, users_groups

load_dotenv()

app = Flask("app")
db = SQLAlchemy()
migrate = Migrate(app, db)

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

# db.drop_all()
# db.create_all()

# user1 = users_groups(title='Post The First', content='Content for the first post')
# user2 = users_groups(title='Post The Second', content='Content for the Second post')
# user3 = users_groups(title='Post The Third', content='Content for the third post')

# comment1 = Comment(content='Comment for the first post', post=user1)
# comment2 = Comment(content='Comment for the second post', post=user2)
# comment3 = Comment(content='Another comment for the second post', user_id=2)
# comment4 = Comment(content='Another comment for the first post', user_id=1)

# tag1 = Tag(name='animals')
# tag2 = Tag(name='tech')
# tag3 = Tag(name='cooking')
# tag4 = Tag(name='writing')

# user1.tags.append(tag1)  # Tag the first post with 'animals'
# user1.tags.append(tag4)  # Tag the first post with 'writing'
# user3.tags.append(tag3)  # Tag the third post with 'cooking'
# user3.tags.append(tag2)  # Tag the third post with 'tech'
# user3.tags.append(tag4)  # Tag the third post with 'writing'


# db.session.add_all([user1,user2,user3])
# db.session.add_all([comment1, comment2, comment3, comment4])
# db.session.add_all([tag1, tag2, tag3, tag4])

# db.session.commit()