import pdb
from config import db, mongo
from sqlalchemy import func
from sql_database.models import Field, GroupName
from bson import ObjectId 
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
        field_key = request.form.get('field_key')
        last_field_key = db.session.query(func.max(Field.field_key)).filter_by(group_id=group_id).scalar()
        if last_field_key is None:
            field_key = 1
        else:
            field_key = last_field_key + 1
        if name and dataformat:
            new_field = Field(name=name, description=description, dataformat=dataformat, field_key=field_key, group_id=group_id)
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
        field_key = request.form.get('field_key')
        field.name = name
        field.description = description
        field.dataformat = dataformat
        field.field_key = field_key
        field.group_id = group_id
        db.session.commit()
        flash('The field has been updated successfully!', 'success')
        return redirect(url_for('users_field.all_fields', group_id=group_id))
    return render_template('user_fields/update_fields.html', field=field, group_id=group_id)

@fields_blueprint.route("/groups/<int:group_id>/fields/field_records", methods=["GET","POST"])
def field_records(group_id):
    group = GroupName.query.get(group_id)
    fields = Field.query.filter_by(group_id=group_id).all()
    field_names = []
    for field in fields:
        field_names.append(field.name)
    return render_template('user_fields/field_records.html', group=group, fields=fields, field_names=field_names)

@fields_blueprint.route("/groups/fields/field_records/records", methods=["GET","POST"])
def records():
    if request.method == "POST":
        request_data = dict(request.form)
        record = {}
        for k,v in request_data.items():
            record.update({k:v})
        return redirect(url_for('users_field.get_records'))
    records = mongo.db.records.find()
    return render_template('user_fields/records.html', records=records)

@fields_blueprint.route('/group/field/field_records/records/get_records', methods=["GET"])
def get_records():
    records = mongo.db.records.find() 
    return render_template("user_fields/records.html", records=records)

@fields_blueprint.route('/group/field/field_records/records/delete_records', methods=["GET","POST"])
def delete_records():
        record_id = request.args.get('id')
        bson_id = ObjectId(record_id)
        record = mongo.db.records.find_one({"_id": bson_id})
        if record:
            return record
        return render_template('user_fields/records.html')
    
@fields_blueprint.route('/groups/<int:group_id>/fields/<int:field_id>/delete_fields', methods=['GET',"POST"])
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

@fields_blueprint.route('/groups/fields', methods=["GET", "POST"])
def back_to_group():
    return redirect(url_for('users.group.group'))