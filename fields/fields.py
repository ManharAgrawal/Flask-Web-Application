from dataclasses import field
import pdb
from config import db
from datetime import datetime
from flask_login import current_user
from decorators.decorators import login_required
from notifications.notifications import send_email
from sql_database.models import User, Field, DataFormat, Status
from flask import Blueprint, render_template, request, url_for, redirect, flash

fields_blueprint = Blueprint('users_field', __name__, template_folder='templates/user_fields')

@fields_blueprint.route('/groups/<int:id>/fields', methods=["GET"])
@login_required
def fields(id):
    fields = Field.query.filter_by(group_id=id).all()
    return render_template('user_fields/fields.html', fields=fields, id=id)

@fields_blueprint.route('/groups/<int:id>/create', methods=["GET"])
@login_required
def create_page(id):
    dataformats = DataFormat.query.all()
    status = Status.query.filter_by(group_id=id).all()
    return render_template("user_fields/create.html", id=id, dataformats=dataformats, status=status)

@fields_blueprint.route('/groups/<int:id>/create', methods=["POST"])   
def create(id): 
    name = request.form.get('name')
    description = request.form.get('description')
    dataformats = request.form.get('dataformat')
    created_date = datetime.utcnow()
    

    updated_date = datetime.utcnow()
    required = request.form.get('required')
    new_field = None
    last_field_key = Field.query.filter_by(group_id=id).order_by(Field.field_key).first()
    if last_field_key:
        last_field_key_int = int(last_field_key.field_key.split('_')[1])
        new_field_key_int = last_field_key_int + 1
        field_key = f'field_{new_field_key_int}'
    else:
        field_key = 'field_1'
    existing_field = Field.query.filter_by(name=name, group_id=id).first()
    if existing_field:
        flash("A field with the same name already exists in this group", "Error")
        return redirect(url_for("users_field.create", id=id))
    if name:
        new_field = Field(name=name, description=description, dataformat_id=dataformats, field_key=field_key, group_id=id, created_date=created_date, updated_date=updated_date, required=required)
        db.session.add(new_field)
        db.session.commit()
        user = User.query.get(current_user.id)
        dataformat = new_field.dataformat.name
        subject = "New Field Created"
        body = f"Dear {user.name},\n\nA New field '{new_field.name}' has been created.\n\nField Description: {new_field.description}\n\nField Dataformat: {dataformat}\n\nField Created By: {user.name}\n\nField Created Date: {new_field.created_date}\n\nBest regards,\nThe App Team"
        html_body = render_template("user_fields/field_create.html", user=user, field=new_field, dataformat=dataformat)
        send_email(subject, user, body, html_body)
        flash('Field Created Successfully!', 'success')
        return redirect(url_for('users_field.fields', id=id, new_field_id=new_field.id))
    return render_template("user_fields/create.html", id=id, fields=new_field)

@fields_blueprint.route('/groups/<int:id>/fields/<int:field_id>/update', methods=["GET"])
@login_required
def edit_page(id,field_id):
    field = Field.query.get(field_id)
    dataformats = DataFormat.query.all()
    status = Status.query.filter_by(group_id=id).all()
    return render_template('user_fields/update.html', field=field, id=id, dataformats=dataformats, status=status)

@fields_blueprint.route('/groups/<int:id>/fields/<int:field_id>/update', methods=["POST"])
def update(id, field_id):
    field = Field.query.get(field_id)
    if not field:
        flash('Field not found.', 'error')
        return redirect(url_for('users_field.fields', id=id))
    old_name = field.name
    old_description = field.description
    old_dataformat = field.dataformat.name 
    name = request.form.get('name')
    description = request.form.get('description')
    dataformat_id = request.form.get('dataformat')
    required = request.form.get('required')
    field_key = request.form.get('field_key')
    field.updated_date = datetime.utcnow()
    field.name = name
    field.description = description
    field.dataformat_id = dataformat_id
    field.field_key = field_key
    field.required = required
    db.session.commit()
    user = User.query.get(current_user.id)
    subject = "Field Updated"
    body = f"Dear {user.name},\n\nThe old Field '{old_name}' has been updated.\n\nOld Field Name: {old_name}\nOld Field Description: {old_description}\nOld Field Dataformat: {old_dataformat}\n\nNew Field Name: {field.name}\nNew Field Description: {field.description}\nNew Field Dataformat: {field.dataformat.name}\n\nField Updated By: {user.name}\nField Updated Date: {field.updated_date}\n\nBest regards,\nThe App Team"
    html_body = render_template("user_fields/field_update.html", user=user, old_name=old_name, old_description=old_description, old_dataformat=old_dataformat, field=field)
    send_email(subject, user, body, html_body)
    flash('The Field has been Updated Successfully!', 'success')
    return redirect(url_for('users_field.fields', id=id))

@fields_blueprint.route('/groups/<int:id>/<int:field_id>/delete')
def delete(id,field_id):
    field = Field.query.get(field_id)
    if field:
        db.session.delete(field)
        db.session.commit()
        status_message, status = 'Field deleted succesfully !!!', 'success'
    else:
        status_message, status = 'Error in deleting field !!!', 'error'
    flash(status_message,status)
    return redirect(url_for('users_field.fields',id=id,field_id=field_id))

@fields_blueprint.route('/groups', methods=["GET"])
@login_required
def back_to_group():
    return redirect(url_for('users.group.group'))