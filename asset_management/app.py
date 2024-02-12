from sql_database.models import UserOps
from flask import Flask, render_template, request, redirect, url_for, flash
from uuid import uuid4

app = Flask(__name__)

app.secret_key = 'a7029be58abc4db9a4897f7f66a299b7'

@app.route('/')
def data():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == email:
            flash("You Successfully!!")
            return redirect(url_for('data'))
        else:
            flash("Check your Email and Password")
    return render_template('login.html') 

@app.route('/logout')
def logout():
    return redirect(url_for('loging'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 == password2:
            flash('Sign up Successfully!!', 'success')
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
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/insert_user', methods=['POST'])
def insert_user():
    if request.method == 'POST':
        user_id = request.form[user_id]
        name = request.form['name']
        email = request.form['email']
        contact = int(request.form['contact'])
        salary = int(request.form['salary'])
        department = request.form['department']
        UserOps.insert_user(user_id, name, email, contact, salary, department)
        return redirect(url_for('insert_data.html',user_id=user_id, name=name, email=email, contact=contact, salary=salary, department=department))
    return redirect(url_for('sign_up.html'))

@app.route('/select_user')
def select_user():
    users = UserOps.select_user()
    return render_template('data.html', users=users)

@app.route('/user_data', methods=["GET", "POST"])
def user_data():
    return render_template('data.html')

@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = int(request.form['user_id'])
    new_values = {'name': request.form['name'],'email': request.form['email'],'contact': int(request.form['contact']),'salary': int(request.form['salary']),'department': request.form['department']}
    UserOps.update_user(user_id, new_values)
    return render_template('data.html')

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    UserOps.delete_user(user_id)
    return redirect(url_for('data.html'))

@app.route('/delete_table', methods=['POST'])
def delete_table():
    UserOps.delete_table()
    return redirect(url_for('data.html'))

if __name__ == "__main__":
    app.run(debug=True)