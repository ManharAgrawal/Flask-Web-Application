import pdb
from config import mongo
from bson import ObjectId
from flask_login import current_user
from sql_database.models import GroupName, Field
from flask import Blueprint, render_template, redirect,  request, flash, url_for

records_blueprint = Blueprint('users_records', __name__, template_folder='templates/records')

@records_blueprint.route("/groups/<int:id>/entry", methods=["GET"])
def entry(id):
    group = GroupName.query.get(id)
    fields = Field.query.filter_by(group_id=id).all()
    return render_template('records/entry.html', id=id, group=group, fields=fields)

@records_blueprint.route("/groups/fields/records", methods=["POST"])
def all_records_page():
    request_data = dict(request.form)
    group_id = request_data.pop('group_id')
    user_id = current_user.id
    records = mongo.db.records.find({'group_id': group_id})
    record_data = []
    field_dict = []
    field_names = {}
    records = list(records)
    if records:
        fields = Field.query.filter_by(group_id=group_id).all()
        field_dict = records[0]['field_names']
        for record in records:
            if record['record_data']:
                record_data.append(record['record_data'])
        field_names = [val for val in field_dict.values()]
    return render_template('records/all_records.html', records=record_data, user_id=user_id, group_id=group_id, field_names=field_names)

@records_blueprint.route("/groups/fields/records", methods=["POST"])
def all_records():
    record_data = []
    request_data = dict(request.form)
    group_id = request_data.pop('group_id')
    user_id = current_user.id
    group_id = request.form.get('group_id')
    fields = Field.query.filter_by(group_id=group_id).all()
    field_names = {}
    for field in fields:
        field_names[field.name] = field.name
    records = mongo.db.records.insert_one({'record_data': record_data, 'group_id': group_id, 'user_id': user_id, 'field_names': field_names})
    return render_template('records/all_records.html', record_data=request_data, records=records, user_id=user_id, group_id=group_id, field_names=field_names)

@records_blueprint.route("/groups/records/details", methods=["GET"])
def details():
    group_id = request.args.get('group_id')
    fields = Field.query.filter_by(group_id=group_id).all()
    records = mongo.db.records.find()
    records_data = {}
    for record in records:
        if 'record_data' in record:
            records_data = record.get('record_data')
            break
    field_names = {}
    for field in fields:
        field_names[field.name] = field.name    
    record = {}
    for key, value in zip(field_names.values(), records_data.values()):
        record[key] = value
    return render_template('records/details.html', group_id=group_id, records_data=record, field_names=field_names)

@records_blueprint.route('/groups/<int:id>/fields/', methods=["GET"])
def back_to_fields(id):
    fields = Field.query.filter_by(id=id).all()
    return redirect(url_for('users_field.fields', id=id))

@records_blueprint.route('/group/records/<int:id>' , methods=["DELETE"])
def delete():
    records = request.args.get('id')
    bson_id = ObjectId(records)
    record = mongo.db.records.find_one({"_id": bson_id})
    if record:
        mongo.db.records.delete_one({"_id": bson_id})
        flash("Record deleted successfully", "success")
    else:
        flash("Create A Record Before Deleting", "error")
    group_id = request.form.get('group_id')
    return render_template('records/all_records.html', group_id=group_id)