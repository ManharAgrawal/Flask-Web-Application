import pdb
from bson import ObjectId
from config import collection
from datetime import datetime
from flask_login import current_user
from decorators.decorator import login_required
from notifications.notification import send_email
from sql_database.models import Field, Status, User, GroupName
from flask import Blueprint, render_template, redirect,  request, flash, url_for

records_blueprint = Blueprint('users_records', __name__, template_folder='templates/records')

@records_blueprint.route("/groups/<int:id>/records", methods=["GET"])
@login_required
def records(id):
    fields = Field.query.filter_by(group_id=id).all()
    status = Status.query.filter_by(group_id=id).all()
    return render_template('records/records.html', id=id, fields=fields, status=status)

@records_blueprint.route("/groups/<int:id>/record_list", methods=["GET"])
@login_required
def record_list_page(id):
    user_id = current_user.id
    records = collection.find({'group_id': id})
    record_data = {}
    for record in records:
        if record.get('record_data'):
            record_id = str(record['_id'])
            record_data[record_id] = dict(list(record['record_data'].items())[:5])
            for key, value in record_data[record_id].items():
                if type(value) == str and 'status' in value:
                    if 'status' in value:
                        status_id = value.split("_")[1]
                        status = Status.query.get(status_id)
                        if status:
                            record_data[record_id][key] = status.name
    fields = Field.query.filter_by(group_id=id).limit(5).all()
    return render_template('records/record_list.html', records=record_data, user_id=user_id, group_id=id, field_names=fields)

@records_blueprint.route("/groups/all_records", methods=["POST"])
def all_records():
    request_data = dict(request.form)
    group_id = int(request_data.pop('group_id'))
    user_id = current_user.id
    fields = Field.query.filter_by(group_id=group_id).all()
    for field in fields:
        if field.dataformat.input_type == 'number':
            if field.field_key in request_data:
                value = request_data.get(field.field_key)
                try:
                    request_data[field.field_key] = int(value)
                except ValueError:
                    request_data[field.field_key] = ""
        if field.dataformat.input_type == 'status':
            if field.field_key in request_data:
                status_id = request_data.get(field.field_key)
                try:
                    request_data[field.field_key] = f"status_{status_id}"                    
                except ValueError:
                    request_data[field.field_key] = ""
    collection.insert_one({'record_data': request_data, 'user_id': user_id, 'group_id': group_id, 'created_date':datetime.utcnow()})
    user = User.query.get(current_user.id)
    group = GroupName.query.get(group_id)
    subject = "New Record Created"
    body = f"Dear {user.name},\n\nA new record has been created in group {group.name} with the following values:\n\n{request_data}\n\nBest regards,\nThe App Team"
    html_body = render_template('records/record_create.html', user=user, record_data=request_data, group_name=group.name, datetime=datetime)
    send_email(subject, user.name, body, html_body)
    flash("Record created successfully", "success")
    return redirect(url_for('users_records.record_list_page', id=group_id))

@records_blueprint.route("/groups/details/<string:record_id>", methods=["GET"])
@login_required
def details(record_id):
    record = collection.find_one({'_id': ObjectId(record_id)})
    group_id = record.get('group_id')
    fields = Field.query.filter_by(group_id=group_id).all()
    keys = [field.name for field in fields]
    record_data = record.get('record_data')
    values = list(record_data.values())
    records = {}
    for i in keys:
        value = values[keys.index(i)]
        if type(value) == str and 'status' in value:
            status_id = str(value).split("_")[1]
            status = Status.query.get(status_id)
            if status:
                records[i] = status.name
        else:
            records[i] = value
    return render_template('records/details.html', record_data=records)

@records_blueprint.route('/groups/<int:id>', methods=["GET"])
@login_required
def back_to_fields(id):
    return redirect(url_for('users_field.fields', id=id))

@records_blueprint.route('/group/<int:id>/records/<string:record_id>', methods=["GET"])
def delete(id,record_id):
    try:
        bson_id = ObjectId(record_id)
        record = collection.find_one({"_id": bson_id})
        if record:
            collection.delete_one({"_id": bson_id})
            group_id = record.get('group_id')
            status_message, status = "Record deleted successfully", "success"
        else:
            group_id = None
            status_message, status = "Record not found", "error"
    except:
        group_id = None
        status_message, status = "Invalid ID format", "error"
    flash(status_message, status)
    return redirect(url_for('users_records.record_list_page', id=id))