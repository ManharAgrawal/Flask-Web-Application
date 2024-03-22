import pdb
from config import mongo
from bson import ObjectId
from flask_login import current_user
from sql_database.models import GroupName, Field
from flask import Blueprint, render_template, redirect,  request, flash, url_for

records_blueprint = Blueprint('users_reocrds', __name__, template_folder='templates/records')

@records_blueprint.route("/groups/<int:group_id>/fields/field_records", methods=["GET"])
def field_records(group_id):
    group = GroupName.query.get(group_id)
    fields = Field.query.filter_by(group_id=group_id).all()
    field_names = []
    for field in fields:
        field_names.append(field.name)
    mongo.db.records.insert_one({"group_id": group_id, "field_names": field_names})
    return render_template('records/field_records.html', group_id=group_id, group=group, fields=fields, field_names=field_names)

@records_blueprint.route("/groups/fields/field_records/records", methods=["GET"])
def records_page():
    return render_template("records/records.html")

@records_blueprint.route("/groups/fields/field_records/records", methods=[ "POST"])
def records():
    record_data = []
    request_data = dict(request.form)
    key_arr = []
    for key, value in request_data.items():
        if not (key.startswith("field_") or key.startswith('group')):
            record_data.append(value)
        elif key.startswith("field_"):
            key_arr.append(key)
    my_dict = dict(zip(key_arr, record_data))
    user_id = current_user.id
    group_id = request.form.get('group_id')
    fields = Field.query.filter_by(group_id=group_id).all()
    field_names = {}
    for field in fields:
        field_names[field.name] = field.name
    records = mongo.db.records.insert_one({'record_data':my_dict, 'group_id':group_id, 'user_id':user_id, 'field_names':field_names})
    return render_template('records/records.html', my_dict=my_dict, records=records, user_id=user_id, group_id=group_id, field_names=field_names)

@records_blueprint.route("/groups/fields/records/records_details", methods=["GET"])
def records_details():
    group_id = request.args.get('group_id')
    fields = Field.query.filter_by(group_id=group_id).all()
    records_value = None
    key_value = None
    records = mongo.db.records.find()
    for record in records:
        if 'record_data' in record:
            records_data = record.get('record_data')
    return render_template('records/records_details.html', group_id=group_id, records_data=records_data)

@records_blueprint.route('/groups/<int:group_id>/fields/records', methods=["GET"])
def back_to_fields(group_id):
    fields = Field.query.filter_by(group_id=group_id).all()
    return redirect(url_for('user_fields.all_fields', group_id=group_id))

@records_blueprint.route('/group/fields/field_records/records/delete_records')
def delete_records():
    records = request.args.get('id')
    bson_id = ObjectId(records)
    record = mongo.db.records.find_one({"_id": bson_id})
    if record:
        mongo.db.records.delete_one({"_id": bson_id})
        flash("Record deleted successfully", "success")
    else:
        flash("Create A Record Before Deleting", "error")
    group_id = request.form.get('group_id')
    return render_template('records/records.html', group_id=group_id)