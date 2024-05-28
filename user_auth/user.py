import pdb
from turtle import pd
from sql_database.models import User
from config import db, razorpay_client
from razorpay.errors import BadRequestError 
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user 
from flask import Blueprint, request, render_template, redirect, url_for,flash 
from decorators.decorator import already_email_exists, already_logged_in_user, user_not_found, incorrect_password

user_blueprint = Blueprint('auth', __name__, template_folder='templates/forms')

@user_blueprint.route('/signup', methods=["GET"])
def signup_form():
    return render_template('forms/sign_up.html')

@user_blueprint.route('/signup', methods=['POST'])
@already_email_exists
@already_logged_in_user
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    if name:
        razorpay_customer = razorpay_client.customer.create(data={'name': name, 'email': email})
        razorpay_customer_id = razorpay_customer['id']
        new_user = User(name=name, email=email, password=password, razorpay_customer_id=razorpay_customer_id)
        db.session.add(new_user)
        db.session.commit()
        status_message, status = 'Signed up successfully!', 'success'
        return redirect(url_for('auth.login'))
    flash(status_message, status)
    return render_template('forms/sign_up.html')

@user_blueprint.route('/login',methods=["GET"])
def login_form():
    return render_template('forms/login.html')

@user_blueprint .route('/login', methods=["POST"])
@already_logged_in_user
@user_not_found
@incorrect_password
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        status_message, status = 'Login successful!', 'success'
        return redirect(url_for('users_group.groups', user_id=user.id))
    else:
        status_message, status = 'Incorrect email or password', 'error'
    flash(status_message, status)
    return render_template('forms/login.html')

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))
