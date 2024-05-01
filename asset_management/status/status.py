import pdb
from config import db
from datetime import datetime
from sql_database.models import Status
from flask import Blueprint, render_template, request, redirect, url_for, flash

status_blueprint = Blueprint('groups_status', __name__, template_folder='templates/group_status')

@status_blueprint.route('/groups/<int:id>/status', methods=["GET"])
def status(id):
    status = Status.query.filter_by(group_id=id).all()
    return render_template('group_status/status.html', status=status, id=id)

@status_blueprint.route('/groups/<int:id>/create', methods=["GET"])
def create_page(id):
    return render_template('group_status/create.html', id=id)

@status_blueprint.route('/groups/<int:id>/create', methods=["POST"])
def create(id):
    status = request.form.get('status')
    description = request.form.get('description')
    created_date = datetime.utcnow()
    updated_date = datetime.utcnow()
    new_status = None
    if status:
        new_status = Status(status=status, description=description, created_date=created_date, updated_date=updated_date, group_id=id)
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
def update(id, status_id):
    status = Status.query.get(status_id)
    if status is None:
        flash('Status not found!', 'error')
        return redirect(url_for('groups_status.edit_page', id=id, status_id=status_id))
    
    new_status_value = request.form.get('status')
    description = request.form.get('description')
    status.status = new_status_value
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