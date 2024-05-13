import pdb
import logging
from config import db
from functools import wraps
from datetime import datetime
from flask_login import current_user
from sql_database.models import Status
from flask import Blueprint, render_template, request, redirect, url_for, flash

status_blueprint = Blueprint('groups_status', __name__, template_folder='templates/group_status')

# Ensure that only logged-in users can access the routes
def login_required(func):
    @wraps(func)
    def for_login(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("User is not logged in", "error")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return for_login

# Validate the status name before creating a new status.
def create_status(func):
    @wraps(func)
    def status_decor(*args, **kwargs):
        name = request.form.get('name')
        if not name:
            flash('Name are required to create a new status', 'error')
            return redirect(url_for('groups_status.create_page', id=kwargs['id']))
        return func(*args, **kwargs)
    return status_decor

@status_blueprint.route('/groups/<int:id>/status', methods=["GET"])
@login_required
def status(id):
    status = Status.query.filter_by(group_id=id).all()
    return render_template('group_status/status.html', status=status, id=id)

@status_blueprint.route('/groups/<int:id>/create', methods=["GET"])
def create_page(id):
    return render_template('group_status/create.html', id=id)

@status_blueprint.route('/groups/<int:id>/create', methods=["POST"])
@create_status
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
        flash('Status Created Successfully!!', 'success')
        return redirect(url_for('groups_status.status', id=id))
    return render_template('group_status/create.html', id=id, status=new_status)

@status_blueprint.route('/groups/<int:id>/status/<int:status_id>/update', methods=["GET"])
def edit_page(id, status_id):
    status = Status.query.get(status_id)
    return render_template('group_status/update.html', id=id, status_id=status_id, status=status)

@status_blueprint.route('/groups/<int:id>/status/<int:status_id>/update', methods=["POST"])
@create_status
def update(id, status_id):
    status = Status.query.get(status_id)
    name = request.form.get('name')
    description = request.form.get('description')
    status.name = name
    status.description = description
    status.updated_date = datetime.utcnow()
    db.session.commit()
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
def back_to_group():
    return redirect(url_for('users.group.group'))