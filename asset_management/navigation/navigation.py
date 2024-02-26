from flask import request, render_template, Blueprint

navigate_blueprint = Blueprint('navigations', __name__, template_folder='templates/navigations')

@navigate_blueprint.route('/contact')
def contact():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
    return render_template('navigations/contact.html',name, email, message)

@navigate_blueprint.route('/about')
def about():
    return render_template('navigations/about.html')

@navigate_blueprint.route('/terms')
def terms():
    return render_template('navigations/terms.html')
