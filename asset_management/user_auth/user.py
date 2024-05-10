import re
import pdb
from config import db
from functools import wraps
from sql_database.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, render_template, redirect, url_for,flash

user_blueprint = Blueprint('auth', __name__, template_folder='templates/forms')

# For sign-up

def already_logged_in_user(func):
    # This decorator checks if the current user is already logged in.
    @wraps(func)
    def login_decorator(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in', 'info')
            return redirect(url_for('users_group.groups', user_id=current_user.id))
        return func(*args, **kwargs)
    return login_decorator

def already_email_exists(func):
    # This decorator checks if the email already exists in the database.
    @wraps(func)
    def email_exists(*args, **kwargs):
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User email already exists', 'error')
            return redirect(url_for('auth.signup_form'))
        return func(*args, **kwargs)
    return email_exists

def valid_password(func):
    # This decorator checks if the password is valid.
    @wraps(func)
    def for_password(*args, **kwargs):
        password = request.form['password']
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('auth.signup_form'))
        return func(*args, **kwargs)
    return for_password

# For log-in

def validate_email(func):
    # This decorator check if the email is valid format
    @wraps(func)
    def for_email(*args, **kwargs):
        email = request.form['email']
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            flash('Invalid email format', 'error')
            return redirect(url_for('auth.login_form'))
        return func(*args, **kwargs)
    return for_email

def user_not_found(func):
    # This decorator checks if the email not exists in the database
    @wraps(func)
    def for_user(*args, **kwargs):
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('auth.login_form'))
        return func(*args, **kwargs)
    return for_user

def incorrect_password(func):
    # This decorator checks if the password entered for login, matches the password stored in the database
    @wraps(func)
    def wrong_pwd(*args, **kwargs):
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and not check_password_hash(user.password, password):
            flash('Incorrect password', 'error')
            return redirect(url_for('auth.login_form'))
        return func(*args, **kwargs)
    return wrong_pwd

@user_blueprint.route('/signup', methods=["GET"])   
def signup_form():
    return render_template('forms/sign_up.html')

@user_blueprint.route('/signup', methods=['POST'])
@validate_email
@user_not_found
@incorrect_password
@valid_password
@already_logged_in_user
def signup():
    name = request.form['name']
    email = request.form['email'] 
    user = User.query.filter_by(email=email).first()
    password = request.form['password']
    if user:
        status_message, status = "User email already exists", 'error'
    else:
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        status_message, status = 'Signed up successfully!', 'success'
        return redirect(url_for('auth.login'))
    flash(status_message, status)
    return render_template('forms/sign_up.html')
    
@user_blueprint.route('/login',methods=["GET"])
def login_form():
    return render_template('forms/login.html')

@user_blueprint.route('/login', methods=["POST"])
@validate_email
@user_not_found
@incorrect_password
@valid_password
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            status_message, status = 'Login successful!', 'success'
            return redirect(url_for('users_group.groups', user_id=user.id))
        else:
            status_message, status = 'Incorrect email or password', 'error'
    else:
        status_message, status = 'User not found', 'error'
    flash(status_message, status)
    return render_template('forms/login.html')

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))