import pdb
from config import db
from flask_login import current_user
from sql_database.models import Profile, User
from notifications.notifications import send_email
from decorators.decorators import login_required, profile_exists
from flask import Blueprint, render_template, redirect,  request, flash, url_for

profile_blueprint = Blueprint('users_profile', __name__, template_folder="template/profile")

@profile_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if profile:
        return render_template('profile/profile.html', profile=profile)
    else:
        return redirect(url_for("users_profile.create"))
    
@profile_blueprint.route("/create", methods=["GET","POST"])
@login_required
@profile_exists('users_profile.profile')
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
            user = User.query.get(current_user.id)
            subject = "New Profile Created"
            body = f"New Profile Created by {current_user.name}\n\nA New Profile name'{new_profile.name}' has been created.\n\nProfile Email: {new_profile.email}\n\nProfile Mobile: {new_profile.mobile}\n\nProfile Address: {new_profile.address}\n\nProfile Position: {new_profile.position}\n\nCreated By: {user.name}\n\nBest regards,\nThe App Team"
            html_body = render_template("profile/profile_create.html", profile=new_profile, user=user)
            send_email(subject, user, body, html_body)
            flash("Profile Created Successfully!", 'success')
            return redirect(url_for("users_profile.profile", new_profile=new_profile))
    return render_template("profile/create.html")

@profile_blueprint.route("/update", methods=["GET","POST"])
@login_required
def update():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if request.method =="POST":
        if profile:
            old_name = profile.name
            old_email = profile.email
            old_mobile = profile.mobile
            old_address = profile.address
            old_position = profile.position
            profile.name = request.form.get('name')
            profile.email = request.form.get('email')
            profile.mobile = request.form.get('mobile')
            profile.address = request.form.get('address')
            profile.position = request.form.get('position')
            db.session.commit()
            user = User.query.get(current_user.id)
            subject = "Profile Updated"
            body = f"Dear {current_user.name},\n\n Profile Name: '{old_name}' has been updated.\n\nA New Profile Name: '{profile.name}'.\n\nOld Email: {old_email} has been updated.\n\nNew Email: {profile.email}\n\nOld Mobile: {old_mobile} has been updated.\n\nNew Mobile: {profile.mobile}\n\nOld Address: {old_address} has been updated.\n\nNew Address: {profile.address}\n\nOld Position: {old_position} has been updated.\n\nNew Position: {profile.position}\n\nCreated By: {user.name}\n\nBest regards,\nThe App Team"
            html_body = render_template("profile/profile_update.html", old_name=old_name, old_email=old_email, old_mobile=old_mobile, old_address=old_address, old_position=old_position, profile=profile, user=user)
            send_email(subject, user, body, html_body)
            flash("Profile Updated Successfully!", 'success')
            return redirect(url_for("users_profile.profile"))
    return render_template("profile/update.html", profile=profile)