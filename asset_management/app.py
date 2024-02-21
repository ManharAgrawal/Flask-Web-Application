import pdb
import uuid #Universally Unique Identifie
from config import db, app
from sql_database.models import User, GroupName
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import  render_template, request, redirect, url_for, flash

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return redirect(url_for('groups'))
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

@app.route('/groups', methods=["GET", "POST"])
def groups():
    if request.method == "POST":
        user_id = current_user.id
        name = request.form.get('name')
        description = request.form.get('description')
        if name and description: 
            new_group = GroupName(name=name, description=description, user=user_id)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created successfully!')
            return redirect(url_for('groups'))
        else:
            flash('Name and description are required.', 'error')
    user = GroupName.query.filter_by(user=current_user.id)
    return render_template('groups.html', entities=user)

@app.route('/text_field',methods=["GET","POST"])    
def text_field():
    return render_template('text_field.html')

@app.route('/update_group/<int:id>',methods=["GET","POST"])
def update_group(id):
    group = GroupName.query.filter_by(id=id)
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        if name and description:
            group.name = name
            group.description = description
            db.session.commit()
            flash("Group updated successfully")
            return redirect(url_for('groups'))
    return render_template('text_field.html',entities=group)

@app.route('/delete_group/<int:id>', methods=['POST'])
def delete_group(id):
    group = GroupName.query.filter_by(id=id)
    if group:
        db.session.delete(group)
        db.session.commit()
        flash('User Data Deleted Successfully')
        return redirect(url_for('groups.html'))
    else:
        flash('User not found', 'error')
    return redirect(url_for('groups.html'))

@app.route('/all_fields', methods=["GET","POST"])
def all_fields():
    return render_template('all_fields.html')

@app.route('/fields',methods=["GET","POST"])
def fields():
    if request.method == "POST":
        name = request.form['name']
        text = request.form['text']
        default = request.form['default']
        return redirect(url_for('all_fields',user_id=user, name=name, text=text, default=default))
    user = GroupName.query.filter_by(user=current_user.id).first()
    return render_template('fields.html',user=user)
    
if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()