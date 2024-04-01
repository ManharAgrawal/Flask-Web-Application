import pdb
from config import mongo
from bson import ObjectId
from flask_login import current_user
from sql_database.models import GroupName, Field
from flask import Blueprint, render_template, redirect,  request, flash, url_for

records_blueprint = Blueprint('users_records', __name__, template_folder='templates/records')

@records_blueprint.route("/groups/<int:id>/records", methods=["GET"])
def records(id):
    group = GroupName.query.get(id)
    fields = Field.query.filter_by(group_id=id).all()
    return render_template('records/records.html', id=id, group=group, fields=fields)

@records_blueprint.route("/groups/<int:id>/record_list", methods=["GET"])
def record_list_page(id):
    request_data = dict(request.form)
    user_id = current_user.id
    group_id = request_data.get('group_id')
    records = mongo.db.records.find({'group_id': str(id)})
    record_data = {}
    for record in records:
        if record.get('record_data'):
            record_id = str(record['_id'])
            record_data[record_id] = record['record_data']
    fields = Field.query.filter_by(group_id=id).all()
    field_names = {}
    for field in fields:
        field_names[field.name] = field.name
    return render_template('records/record_list.html', records=record_data.items(), user_id=user_id, group_id=id, field_names=field_names)

@records_blueprint.route("/groups/all_records", methods=["POST"])
def all_records():
    request_data = dict(request.form)
    group_id = request_data.pop('group_id')
    user_id = current_user.id
    fields = Field.query.filter_by(group_id=group_id).all()
    field_names = {}
    for field in fields:
        field_names[field.name] = field.name   
    records = {}
    for key, val in zip(field_names.values(), request_data.values()):
        records[key] = val 
    mongo.db.records.insert_one({'record_data': records, 'user_id': user_id, 'group_id': group_id})
    return redirect(url_for('users_records.record_list_page', id=group_id))

@records_blueprint.route("/groups/details", methods=["GET"])
def details():
    group_id = request.args.get('group_id')
    records = mongo.db.records.find({'group_id': group_id})
    field_names = {}
    fields = Field.query.filter_by(group_id=group_id).all()
    for field in fields:
        field_names[field.name] = field.name    
    record_data = []
    for record in records:
        if 'record_data' in record:
            record_data.append(record.get('record_data'))
    return render_template('records/details.html', group_id=group_id, record_data=record_data, field_names=field_names)

@records_blueprint.route('/groups/<int:id>', methods=["GET"])
def back_to_fields(id):
    fields = Field.query.filter_by(id=id).all()
    return redirect(url_for('users_field.fields', id=id))

from bson import ObjectId

@records_blueprint.route('/group/records/<string:id>', methods=["GET"])
def delete(id):
    try:
        bson_id = ObjectId(id)
        record = mongo.db.records.find_one({"_id": bson_id})
        if record:
            mongo.db.records.delete_one({"_id": bson_id})
            flash("Record deleted successfully", "success")
            group_id = record.get('group_id')
        else:
            flash("Record not found", "error")
            group_id = None
    except:
        flash("Invalid ID format", "error")
        group_id = None
    
    return redirect(url_for('users_records.record_list_page', id=id))