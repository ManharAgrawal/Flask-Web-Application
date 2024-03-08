import pdb
from config import db
from sql_database.models import User
from werkzeug.security import check_password_hash
from services.flash import flash_for_users
from flask_login import login_user, login_required, logout_user
from flask import Blueprint, request, render_template, redirect, url_for, flash

user_blueprint = Blueprint('auth', __name__, template_folder='templates/forms')

@user_blueprint.route('/signup', methods=["GET",'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'] 
        user = User.query.filter_by(email= email).first()
        password1 = request.form['password1']
        password2 = request.form['password2']
        if user:
            flash_for_users("User Email already Exists", 'error')
        elif password1 == password2:
            user = User(name=name, email=email, password=password1)
            db.session.add(user)
            db.session.commit()
            flash_for_users('Signed Up Successfully!!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash_for_users('Passwords do not match. Please try again.', 'error')
    return render_template('forms/sign_up.html')

@user_blueprint.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password =  request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user, remember=True)
            flash_for_users('Login successful!','success')
            return redirect(url_for('users_group.groups',user_id=user.id))
        else:
            flash_for_users('Invalid email or password', 'error')
    return render_template('forms/login.html')

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash_for_users('You have been logged out', 'success')
    return redirect(url_for('auth.login'))