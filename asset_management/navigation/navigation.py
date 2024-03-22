from flask import request, redirect, url_for, Blueprint, flash, render_template

navigate_blueprint = Blueprint('navigate', __name__, template_folder='templates/navigations')

@navigate_blueprint.route('/user/contact', methods=["GET"])
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
def about():
    return render_template('navigations/about.html')

@navigate_blueprint.route('/user/terms', methods=["GET"])
def terms():
    return render_template('navigations/terms.html')