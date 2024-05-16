import pdb
import logging
from config import db
from datetime import datetime
from flask_login import current_user
from sql_database.models import Status, User
from notifications.notification import send_email
from decorators.decorator import login_required 
from flask import Blueprint, render_template, request, redirect, url_for, flash

status_blueprint = Blueprint('groups_status', __name__, template_folder='templates/group_status')

@status_blueprint.route('/groups/<int:id>/status', methods=["GET"])
@login_required
def status(id):
    status = Status.query.filter_by(group_id=id).all()
    return render_template('group_status/status.html', status=status, id=id)

@status_blueprint.route('/groups/<int:id>/create', methods=["GET"])
@login_required
def create_page(id):
    return render_template('group_status/create.html', id=id)

@status_blueprint.route('/groups/<int:id>/create', methods=["POST"])
def create(id):
    name = request.form.get('name')
    description = request.form.get('description')
    created_date = datetime.utcnow()
    updated_date = datetime.utcnow()
    new_status = None
    if status:
        new_status = Status(name=name, description=description, created_date=created_date, updated_date=updated_date, group_id=id)
        db.session.add(new_status)
        db.session.commit()
        user = User.query.get(current_user.id)
        subject = "New Status Created"
        body = f"Dear {user.name},\n\nA new status name'{new_status.name}' has been created.\n\nDescription: {new_status.description}\n\nCreated By: {user.name}\n\nCreated Date: {new_status.created_date}\n\nBest regards,\nThe App Team"
        send_email(subject, user, body)
        flash('Status Created Successfully!!', 'success')
        return redirect(url_for('groups_status.status', id=id))
    return render_template('group_status/create.html', id=id, status=new_status)

@status_blueprint.route('/groups/<int:id>/status/<int:status_id>/update', methods=["GET"])
@login_required
def edit_page(id, status_id):
    status = Status.query.get(status_id)
    return render_template('group_status/update.html', id=id, status_id=status_id, status=status)

@status_blueprint.route('/groups/<int:id>/status/<int:status_id>/update', methods=["POST"])
def update(id, status_id):
    status = Status.query.get(status_id)
    old_name = status.name
    old_description = status.description
    name = request.form.get('name')
    description = request.form.get('description')
    status.name = name
    status.description = description
    status.updated_date = datetime.utcnow()
    db.session.commit()
    user = User.query.get(current_user.id)
    subject = "Status Updated"
    body = f"Dear {user.name},\n\nThe status '{old_name}' has been updated.\n\nOld Name: {old_name}\nOld Description: {old_description}\n\nNew Name: {status.name}\nNew Description: {status.description}\n\nUpdated By: {user.name}\nUpdated Date: {status.updated_date}\n\nBest regards,\nThe App Team"
    send_email(subject, user, body)
    flash('The status has been updated successfully!', 'success')
    return redirect(url_for('groups_status.status', id=id, status_id=status_id))

@status_blueprint.route('/groups/<int:id>/status/<int:status_id>/delete')
def delete(id,status_id):
    status = Status.query.get(status_id)
    if status:
        db.session.delete(status)
        db.session.commit()
        status_message, status = 'Status deleted succesfully !!!', 'success'
    else:
        status_message, status = 'Error in deleting status !!!', 'error'
    flash(status_message,status)
    return redirect(url_for('groups_status.status', id=id,status_id=status_id))

@status_blueprint.route('/groups', methods=["GET"])
@login_required
def back_to_group():
    return redirect(url_for('users.group.group'))