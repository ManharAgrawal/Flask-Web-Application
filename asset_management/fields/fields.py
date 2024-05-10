import pdb
from flask_login import current_user
from config import db
from functools import wraps
from datetime import datetime
from sql_database.models import Field, DataFormat, Status
from flask import Blueprint, render_template, request, url_for, redirect, flash

fields_blueprint = Blueprint('users_field', __name__, template_folder='templates/user_fields')

def login_required(func):
    # Ensure that only logged-in users can access the routes
    @wraps(func)
    def for_login(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("User is not logged in", "error")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return for_login

@fields_blueprint.route('/groups/<int:id>/fields', methods=["GET"])
@login_required
def fields(id):
    fields = Field.query.filter_by(group_id=id).all()
    return render_template('user_fields/fields.html', fields=fields, id=id)

@fields_blueprint.route('/groups/<int:id>/create', methods=["GET"])
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
    last_field_key = Field.query.filter_by(group_id=id).order_by(Field.field_key.desc()).first()
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
    if name and dataformats:
        new_field = Field(name=name, description=description, dataformat_id=dataformats, field_key=field_key, group_id=id, created_date=created_date, updated_date=updated_date, required=required)
        db.session.add(new_field)
        db.session.commit()
        flash('Field Created Successfully!', 'success')
        return redirect(url_for('users_field.fields', id=id, new_field_id=new_field.id))
    return render_template("user_fields/create.html", id=id, fields=new_field)

@fields_blueprint.route('/groups/<int:id>/fields/<int:field_id>/update', methods=["GET"])
def edit_page(id,field_id):
    field = Field.query.get(field_id)
    dataformats = DataFormat.query.all()
    status = Status.query.filter_by(group_id=id).all()
    return render_template('user_fields/update.html', field=field, id=id, dataformats=dataformats, status=status)

@fields_blueprint.route('/groups/<int:id>/fields/<int:field_id>/update', methods=["POST"])
def update(id, field_id):
    field = Field.query.get(field_id)
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
    flash('The field has been updated successfully!', 'success')
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
def back_to_group():
    return redirect(url_for('users.group.group'))