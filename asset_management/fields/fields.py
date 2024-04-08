import pdb
from config import db, mongo
from sqlalchemy import func
from datetime import datetime
from sql_database.models import Field, DataFormat
from flask import Blueprint, render_template, request, url_for, redirect, flash

fields_blueprint = Blueprint('users_field', __name__, template_folder='templates/user_fields')

@fields_blueprint.route('/groups/<int:id>/fields', methods=["GET"])
def fields(id):
    fields = Field.query.filter_by(group_id=id).all()
    return render_template('user_fields/fields.html', fields=fields, id=id)

@fields_blueprint.route('/groups/<int:id>/create', methods=["GET"])
def create_page(id):
    dataformats = DataFormat.query.all()
    return render_template("user_fields/create.html", id=id, dataformats=dataformats)

@fields_blueprint.route('/groups/<int:id>/create', methods=["POST"])   
def create(id):
    name = request.form.get('name')
    description = request.form.get('description')
    dataformats = request.form.get('dataformat')
    created_date = datetime.utcnow()
    updated_date = datetime.utcnow()
    new_field = None
    last_field_key = db.session.query(func.max(Field.field_key)).filter_by(group_id=id).scalar()
    if last_field_key is None:
        field_key = 'field_1'
    else:
        last_field_key_int = int(last_field_key.split('_')[1])
        new_field_key_int = last_field_key_int + 1
        field_key = f'field_{new_field_key_int}'
    if name and dataformats:
        new_field = Field(name=name, description=description, dataformat_id=dataformats, field_key=field_key, group_id=id, created_date=created_date, updated_date=updated_date)
        db.session.add(new_field)
        db.session.commit()
        flash('Field Created Successfully!', 'success')
        return redirect(url_for('users_field.fields', id=id, new_field_id=new_field.id))
    return render_template("user_fields/create.html", id=id, fields=new_field)

@fields_blueprint.route('/groups/<int:id>/fields/<int:field_id>/update', methods=["GET"])
def update_page(id,field_id):
    field = Field.query.get(field_id)
    dataformats = DataFormat.query.all()
    return render_template('user_fields/update.html', field=field, id=id, dataformats=dataformats)
    
@fields_blueprint.route('/groups/<int:id>/fields/<int:field_id>/update', methods=["POST"])
def update(id, field_id):
    field = Field.query.get(field_id)
    name = request.form.get('name')
    description = request.form.get('description')
    dataformat_id = request.form.get('dataformat')
    field_key = request.form.get('field_key')
    field.updated_date = datetime.utcnow() 
    field.name = name
    field.description = description
    field.dataformat_id = dataformat_id
    field.field_key = field_key
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