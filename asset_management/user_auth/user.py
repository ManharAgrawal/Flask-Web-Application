import pdb
from config import app,db
from sql_database.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user
from flask import Blueprint, request, render_template, redirect, url_for, flash

user_blueprint = Blueprint('auth', __name__, template_folder='templates/forms')

@user_blueprint.route('/signup', methods=["GET",'POST'])
def signup():
    print(request.method)
    if request.method == 'POST':
        # pdb.set_trace()      
        name = request.form['name']
        email = request.form['email'] 
        user = User.query.filter_by(email= email).first()
        password1 = request.form['password1']
        password2 = request.form['password2']
        if user:
            flash("User Email already Exists")
        elif password1 == password2:
            flash('Signed Up Successfully!!', 'success')
            user = User(name=name, email=email, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('Passwords do not match. Please try again.', 'error')
    return render_template('forms/sign_up.html')

@user_blueprint.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password =  request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user, remember=True)
            flash('Login successful!','success')
            return redirect(url_for('users_group.groups'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('forms/login.html')

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))