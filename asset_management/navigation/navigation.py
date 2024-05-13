from flask import request, redirect, url_for, Blueprint, flash, render_template
from functools import wraps
from flask_login import current_user

navigate_blueprint = Blueprint('navigate', __name__, template_folder='templates/navigations')

# Ensure that only logged-in users can access the routes
def login_required(func):
    @wraps(func)
    def for_login(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("User is not logged in", "error")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return for_login

@navigate_blueprint.route('/user/contact', methods=["GET"])
@login_required
def contact_page():
    name = ""
    email = ""
    message = ""
    return render_template('navigations/contact.html', name=name, email=email, message=message)
    
@navigate_blueprint.route('/user/contact', methods=["POST"])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    flash('Message sent successfully!')
    return redirect(url_for('navigate.contact', name=name, email=email, message=message))

@navigate_blueprint.route('/user/about', methods=["GET"])
@login_required
def about():
    return render_template('navigations/about.html')

@navigate_blueprint.route('/user/terms', methods=["GET"])
@login_required
def terms():
    return render_template('navigations/terms.html')