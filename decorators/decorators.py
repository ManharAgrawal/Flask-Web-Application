
from functools import wraps
from flask_login import current_user
from config import db, razorpay_client
from sql_database.models import User, Profile
from werkzeug.security import check_password_hash
from flask import redirect, url_for, request, flash

# For Sign-Up

# This decorator checks if the current user is already logged in.
def already_logged_in_user(func):
    @wraps(func)
    def for_login(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in', 'error')
            return redirect(url_for('auth.login', user_id=current_user.id))
        return func(*args, **kwargs)
    return for_login

# This decorator checks if the email already exists in the database.
def already_email_exists(func):
    @wraps(func)
    def email_exists(*args, **kwargs):
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User email already exists', 'error')
            return redirect(url_for('auth.signup'))
        return func(*args, **kwargs)
    return email_exists

# For log-in

# This decorator checks if the email not exists in the database
def user_not_found(func):
    @wraps(func)
    def for_user(*args, **kwargs):
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return for_user

# This decorator checks if the password entered for login, matches the password stored in the database
def incorrect_password(func):
    @wraps(func)
    def wrong_pwd(*args, **kwargs):
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and not check_password_hash(user.password, password):
            flash('Incorrect password', 'error')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrong_pwd

# Ensure that only logged-in users can access the routes
def login_required(func):
    @wraps(func)
    def for_login(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("User is not logged in", "error")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return for_login

# This decorator ensures that a database session exists before connecting to APIs.
def for_database(func):
    @wraps(func)
    def database(*args, **kwargs):
        if db.session is None:
            flash("Database session is not initialized")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return database

# If a profile already exists for the current user before allowing them to create a new one
def profile_exists(redirect_url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            profile = Profile.query.filter_by(user_id=current_user.id).first()
            if profile:
                flash('Profile Already Exists.')
                return redirect(url_for(redirect_url))
            return func(*args, **kwargs)
        return wrapper
    return decorator