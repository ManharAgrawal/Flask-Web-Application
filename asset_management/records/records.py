import pdb
from config import mongo
from bson import ObjectId
from datetime import datetime
from flask_login import current_user
from sql_database.models import User, GroupName, Field
from flask import Blueprint, render_template, redirect,  request, flash, url_for

records_blueprint = Blueprint('users_records', __name__, template_folder='templates/records')

@records_blueprint.route("/groups/<int:id>/records", methods=["GET"])
def records(id):
    fields = Field.query.filter_by(group_id=id).all()
    return render_template('records/records.html', id=id, fields=fields)

@records_blueprint.route("/groups/<int:id>/profile", methods=["GET"])
def profile(id):
    user = User.query.filter_by(id=current_user.id).first()
    groups = GroupName.query.filter_by(user_id=user.id).all()
    group_ids = []
    for group in groups:
        group_ids.append(group.id)
    fields = Field.query.all()
    user_fields = []
    for field in fields:
        if field.group_id:
            user_fields.append(field)
    user_records = mongo.db.record.find({"group_id": str(id)})
    return render_template('records/profile.html', user=user, user_groups=groups, user_fields=user_fields, user_records=user_records, id=id)

@records_blueprint.route("/groups/<int:id>/record_list", methods=["GET"])
def record_list_page(id):
    user_id = current_user.id
    records = mongo.db.records.find({'group_id': str(id)})
    record_data = {}
    for record in records:
        if record.get('record_data'):
            record_id = str(record['_id'])
            record_data[record_id] = dict(list(record['record_data'].items())[:5])
    fields = Field.query.filter_by(group_id=id).limit(5).all()
    record = record_data
    return render_template('records/record_list.html', records=record, user_id=user_id, group_id=id, field_names=fields)

@records_blueprint.route("/groups/all_records", methods=["POST"])
def all_records():
    request_data = dict(request.form)
    group_id = request_data.pop('group_id')
    user_id = current_user.id
    fields = Field.query.filter_by(group_id=group_id).all()
    for field in fields:
        if field.dataformat.input_type == 'number':
            if field.field_key in request_data:
                value = request_data.get(field.field_key)
                request_data[field.field_key] = int(value)
    mongo.db.records.insert_one({'record_data': request_data, 'user_id': user_id, 'group_id': group_id, 'created_date':datetime.utcnow()})
    return redirect(url_for('users_records.record_list_page', id=group_id))

@records_blueprint.route("/groups/details/<string:record_id>", methods=["GET"])
def details(record_id):
    record = mongo.db.records.find_one({'_id': ObjectId(record_id)})
    group_id = record.get('group_id')
    fields = Field.query.filter_by(group_id=group_id).all()
    keys = [field.name for field in fields]
    record_data = record.get('record_data')
    values = list(record_data.values())
    records = {}
    for i in keys:
        records[i] = values[keys.index(i)]
    return render_template('records/details.html', record_data=records)

@records_blueprint.route('/groups/<int:id>', methods=["GET"])
def back_to_fields(id):
    return redirect(url_for('users_field.fields', id=id))

@records_blueprint.route('/group/<int:id>/records/<string:record_id>', methods=["GET"])
def delete(id,record_id):
    try:
        bson_id = ObjectId(record_id)
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