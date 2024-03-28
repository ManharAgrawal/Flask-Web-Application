import pdb
from config import db
from sqlalchemy import func
from sql_database.models import Field
from flask import Blueprint, render_template, request, url_for, redirect, flash

fields_blueprint = Blueprint('users_field', __name__, template_folder='templates/user_fields')

@fields_blueprint.route('/groups/<int:id>/fields', methods=["GET"])
def fields(id):
    fields = Field.query.filter_by(group_id=id).all()
    return render_template('user_fields/fields.html', fields=fields, id=id)

@fields_blueprint.route('/groups/<int:id>/fields/create', methods=["GET"])
def create_page(id):
    return render_template("user_fields/create.html", id=id)

@fields_blueprint.route('/groups/<int:id>/fields/create', methods=["POST"])   
def create(id):
    name = request.form.get('name')
    description = request.form.get('description')
    dataformat = request.form.get('dataformat')
    field_key = request.form.get('field_key')
    last_field_key = db.session.query(func.max(Field.field_key)).filter_by(id=id).scalar()
    if last_field_key is None:
        field_key = 'field_1'
    else:
        last_field_key_int = int(last_field_key.split('_')[1])
        new_field_key_int = last_field_key_int + 1
        field_key = f'field_{new_field_key_int}'
    if name and dataformat:
        new_field = Field(name=name, description=description, dataformat=dataformat, field_key=field_key, group_id=id)
        db.session.add(new_field)
        db.session.commit()
        flash('Field Created Successfully!', 'success')
        return redirect(url_for('users_field.fields', id=id))
    
    return render_template("user_fields/create.html", id=id, fields=new_field)

@fields_blueprint.route('/groups/<int:id>/fields/<int:field_id>/update', methods=["GET"])
def update_page(id,field_id):
    field = Field.query.get(field_id)
    return render_template('user_fields/update.html', field=field, id=id)
    
@fields_blueprint.route('/groups/<int:id>/fields/<int:field_id>/update', methods=["POST"])
def update(id, field_id):
    field = Field.query.get(field_id)
    name = request.form.get('name')
    description = request.form.get('description')
    dataformat = request.form.get('dataformat')
    field_key = request.form.get('field_key')
    field.name = name
    field.description = description
    field.dataformat = dataformat
    field.field_key = field_key
    field.id = id
    db.session.commit()
    flash('The field has been updated successfully!', 'success')
    return redirect(url_for('users_field.fields', id=id))

@fields_blueprint.route('/groups/<int:id>/fields/<int:field_id>/delete')
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

@fields_blueprint.route('/groups/fields', methods=["GET"])
def back_to_group():
    return redirect(url_for('users.group.group'))