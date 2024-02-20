import pdb
import uuid #Universally Unique Identifie
from werkzeug.security import check_password_hash
from flask import  render_template, request, redirect, url_for, flash
from config import db, app
from sql_database.models import User
from flask_login import login_user, login_required, logout_user

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html') 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST',"GET"])
def signup():
    print(request.method)
    if request.method == 'POST':
        name = request.form['name']
        user = User.query.filter_by(email= request.form['email']).first()
        email = request.form['email'] 
        password1 = request.form['password1']
        password2 = request.form['password2']
        if user:
            flash("User Email already Exists")
        elif password1 == password2:
            flash('Signed Up Successfully!!', 'success')
            user = User(name=name, email=email, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match. Please try again.', 'error')
    return render_template('sign_up.html')

@app.route('/contact')
def contact():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
    return render_template('contact.html',name, email, message)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/index', methods=["GET","POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        discription = request.form['discription']
        return render_template('index.html')
    return render_template('index.html')

@app.route('/text_field',methods=["GET","POST"])
def text_field():
    if request.method == "POST":
        name = request.form['name']
        discription = request.form['discription']
        return redirect(url_for('index'))
    return render_template('text_field.html')
    
if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()