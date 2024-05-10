import pdb
from config import db
from functools import wraps
from flask_login import current_user
from sql_database.models import Profile
from flask import Blueprint, render_template, redirect,  request, flash, url_for

profile_blueprint = Blueprint('users_profile', __name__, template_folder="template/profiles")

def login_required(func):
    # Ensure that only logged-in users can access the routes
    @wraps(func)
    def for_login(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("User is not logged in", "error")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return for_login

def profile_exists(func):
    # if a profile already exists for the current user before allowing them to create a new one
    @wraps(func)
    def profiles_decor(*args, **kwargs):
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if profile:
            flash('Profile already exists.')
            return redirect(url_for('users_profile.profile'))
        return func(*args, **kwargs)
    return profiles_decor

@profile_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if profile:
        return render_template('profiles/profile.html', profile=profile)
    else:
        return redirect(url_for("users_profile.create"))

@profile_blueprint.route("/create", methods=["GET","POST"])
@login_required
@profile_exists
def create():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        address = request.form.get('address')
        position = request.form.get('position')
        if name and email:
            new_profile = Profile(name=name, email=email, mobile=mobile, address=address, position=position, user_id=current_user.id)
            db.session.add(new_profile)
            db.session.commit()
            flash("Profile Created Successfully!", 'success')
            return redirect(url_for("users_profile.profile", new_profile=new_profile))
    return render_template("profiles/create.html")

@profile_blueprint.route("/update", methods=["GET","POST"])
@login_required
def update():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if request.method =="POST":
        if profile:
            profile.name = request.form.get('name')
            profile.email = request.form.get('email')
            profile.mobile = request.form.get('mobile')
            profile.address = request.form.get('address')
            profile.position = request.form.get('position')
            db.session.commit()
            flash("Profile Updated Successfully!", 'success')
            return redirect(url_for("users_profile.profile"))
    return render_template("profiles/update.html", profile=profile)