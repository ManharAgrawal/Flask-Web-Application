import pdb
import uuid #Universally Unique Identifie
from config import db, app
from sql_database.models import User, GroupName, Field
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
        email = request.form['email'] 
        user = User.query.filter_by(email= request.form['email']).first()
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
        if user_id: 
            new_group = GroupName(name=name, description=description, user=user_id)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created successfully!')
            return redirect(url_for('groups'))
        else:
            flash('Name and description are required.')
    user = GroupName.query.filter_by(user=current_user.id)
    return render_template('groups.html', entities=user)

@app.route('/text_field',methods=["GET","POST"])    
def text_field():
    return render_template('text_field.html')

@app.route('/update_group/<int:id>',methods=["GET","POST"])
def update_group(id):
    group = GroupName.query.get(id)
    if request.method == "POST":
        id = request.form.get('id')
        name = request.form.get('name')
        description = request.form.get('description')
        if group:
            group.name = name
            group.description = description
            db.session.add(group)
            db.session.commit()
            flash("Group updated successfully")
            return redirect(url_for('groups'))
    return render_template('text_field.html',entity=group)

@app.route('/delete_group/<int:id>', methods=['GET',"POST"])
def delete_group(id):
    group = GroupName.query.filter_by(id=id).first()
    if group:
        db.session.delete(group)
        db.session.commit()
        flash('Group Data Deleted Successfully')
        return redirect(url_for('groups'))
    else:
        flash('Group not found')
    return redirect(url_for('groups'))

@app.route('/all_fields', methods=["GET","POST"])
def all_fields():
    if request.method == "POST":
        group_id = request.form.get('group')
        name = request.form.get('name')
        text = request.form.get('text')
        default = request.form.get('default')
        if group_id:
            new_field = Field(name=name, text=text, default=default, group_name_id=group_id)
            db.session.add(new_field)
            db.session.commit()
            flash('Group field created successfully!')
            return redirect(url_for('all_fields'))
        else:
            flash('Group Not Found')
    field = Field.query.all()
    return render_template('all_fields.html', field=field)

@app.route('/group_fields', methods=["GET", "POST"])
def group_fields():
    groups = GroupName.query.all()
    return render_template('group_fields.html', groups=groups)

@app.route('/update_field/<int:id>', methods=["GET","POST"])
def update_field(id): 
    field = Field.query.get(id)
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        field.name = name
        field.description = description
        db.session.add(field)
        db.session.commit()
        flash("Group updated successfully")
        return redirect(url_for('all_fields'))
    return render_template('group_fields.html',fields=field)

@app.route('/delete_field/<int:id>', methods=["GET","POST"])
def delete_field(id):
    field = Field.query.filter_by(id=id).first()
    if field:
        db.session.delete(field)
        db.session.commit()
        flash('Group Data Deleted Successfully')
        return redirect(url_for('all_fields'))
    else:
        flash('Group not found')
    return redirect(url_for('all_fields'))

if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()