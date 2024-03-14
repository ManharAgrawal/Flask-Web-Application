from config import db, mongo
from sql_database.models import Field
from bson.objectid import ObjectId 
from flask import Blueprint, render_template, request, url_for, redirect, flash

fields_blueprint = Blueprint('users_field', __name__, template_folder='templates/user_fields')

@fields_blueprint.route('/groups/<int:group_id>/all_fields', methods=["GET","POST"])
def all_fields(group_id):
    fields = Field.query.filter_by(group_id=group_id).all()
    return render_template('user_fields/all_fields.html', fields=fields, group_id=group_id)

@fields_blueprint.route('/groups/<int:group_id>/fields/create_field', methods=["GET", "POST"])   
def create_field(group_id):
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        dataformat = request.form.get('dataformat')
        if dataformat == 'Integer':
            flag = 'Integer'
        elif dataformat == 'String':
            flag = 'String'
        else:
            flag = 'Boolean'
        if name and description and dataformat:
            new_field = Field(name=name, description=description, dataformat=flag, group_id=group_id)
            db.session.add(new_field)
            db.session.commit() 
            flash('Field Created Successfully!', 'success')
            return redirect(url_for('users_field.all_fields', group_id=group_id))
    return render_template("user_fields/create_field.html", group_id=group_id)

@fields_blueprint.route('/groups/<int:group_id>/fields/<int:field_id>/update_fields', methods=["GET", "POST"])
def update_fields(group_id, field_id):
    field = Field.query.get(field_id)
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        dataformat = request.form.get('dataformat')
        field.name = name
        field.description = description
        field.dataformat = dataformat
        field.group_id = group_id
        db.session.commit()
        flash('The field has been updated successfully!', 'success')
        return redirect(url_for('users_field.all_fields', group_id=group_id))
    return render_template('user_fields/update_fields.html', field=field, group_id=group_id)

@fields_blueprint.route("/groups/fields/field_records", methods=["GET","POST"])
def field_records():
    if request.method == "POST":
        name = {"Field Name":"field.name"}
        dataformat = {"Field Dataformat":"field.dataformat"}
        records = mongo.db.inventory.insert_one({"Field Name":name, "Field Dataformat":dataformat})
        return render_template('user_fields/field_records.html', records=records)
    fields = Field.query.all()
    field_names = []
    for field in fields:
        field_names.append(field.name)
    return render_template('user_fields/field_records.html', fields=fields, field_names=field_names)

@fields_blueprint.route('/groups/<int:group_id>/fields/<int:field_id>/delete_fields>', methods=['GET',"POST"])
def delete_fields(group_id,field_id):
    field = Field.query.get(field_id)
    if field:
        db.session.delete(field)
        db.session.commit()
        status_message, status = 'Field deleted succesfully !!!', 'success'
    else:
        status_message, status = 'Error in deleting field !!!', 'error'
    flash(status_message,status)
    return redirect(url_for('users_field.all_fields',group_id=group_id,field_id=field_id))

@fields_blueprint.route('/groups/groups',methods=["GET","POST"])
def back_to_group():
    return redirect(url_for('users_group.groups'))
