from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'crud_app.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, contact TEXT NOT NULL, city TEXT NOT NULL)")
    conn.commit()
    conn.close()

@app.route('/')
def show_data():
    create_table()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('show_data.html', users=users)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        city = request.form['city']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, contact, city) VALUES (?, ?, ?, ?)', (name, email, contact, city))
        conn.commit()
        conn.close()
        return redirect(url_for('show_data'))
    return render_template('create_data.html')

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('create_data.html', form_method='POST', form_action=url_for('update_user', user_id=user_id), entry=user)

@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    name = request.form['name']
    email = request.form['email']
    contact = request.form['contact']
    city = request.form['city']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name=?, email=?, contact=?, city=? WHERE id=?', (name, email, contact, city, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('show_data'))


@app.route('/delete/<int:user_id>')
def delete(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('show_data'))

if __name__ == '__main__':
    app.run(debug=True)