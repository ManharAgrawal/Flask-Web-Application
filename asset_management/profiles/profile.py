import pdb
from config import db
from flask_login import current_user
from sql_database.models import Profile
from flask import Blueprint, render_template, redirect,  request, flash, url_for

profile_blueprint = Blueprint('users_profile', __name__, template_folder="template/user_profiles")

@profile_blueprint.route("/profile/<int:user_id>", methods=["GET"])
def profile(user_id):
    user_id = current_user.id
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if profile:
        return render_template('user_profiles/profile.html', profile=profile, user_id=user_id)
    else:
        return redirect(url_for("users_profile.create"))

@profile_blueprint.route("/create", methods=["GET","POST"])
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
    return render_template("user_profiles/create.html")

@profile_blueprint.route("/update", methods=["GET","POST"])
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
    return render_template("user_profiles/update.html")

@profile_blueprint.route("/groups", methods=["GET"])
def groups():
    return redirect(url_for('users_group.groups'))

@profile_blueprint.route("/delete", methods=["GET"])
def delete():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if profile:
        db.session.delete(profile)
        db.session.commit()
        status_message, status = "Profile Deleted Successfully!!", 'success'
    else:
        status_message, status = "Error in Deleteing Profile", 'error'
    flash(status_message,status)
    return render_template('user_profiles/profile')