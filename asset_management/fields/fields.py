from config import db
from sql_database.models import Field, GroupName
from services.flash import flash_for_fields
from flask import Blueprint, render_template, request, flash, url_for, redirect

fields_blueprint = Blueprint('users_field', __name__, template_folder='templates/user_fields')

@fields_blueprint.route('/groups/<int:group_id>/all_fields', methods=["GET","POST"])
def all_fields(group_id):
    fields = Field.query.filter_by(group_name_id=group_id).all()
    return render_template('user_fields/all_fields.html', fields=fields, group_id=group_id)

@fields_blueprint.route('/groups/<int:group_id>/fields/create_fields',methods=["GET","POST"])
def create_fields(group_id):
    if request.method=="POST":
        name = request.form.get('name')
        text = request.form.get('text')
        is_default = request.form.get('is_default')
        if is_default=="True":
            flag = True
        else:
            flag = False
        new_field = Field(name=name, text=text, is_default=flag, group_name_id=group_id)
        db.session.add(new_field)
        db.session.commit() 
        flash_for_fields('Field Created Successfully!', 'success')
        return redirect(url_for('users_field.all_fields', group_id=group_id))
    else:
        group = GroupName.query.all()
        context = {"groups":group}
        flash_for_fields('Invalid email or password', 'error')
    return render_template("user_fields/text_field.html",**context,group_id=group_id) 

@fields_blueprint.route('/groups/<int:group_id>/fields/<int:field_id>/update_fields', methods=["GET", "POST"])
def update_fields(group_id, field_id):
    field = Field.query.get(field_id)
    if request.method == "POST":
        name = request.form.get('name')
        text = request.form.get('text')
        is_default = request.form.get('is_default')
        if is_default.lower() == 'true':
            is_default = True
        else:
            is_default = False
        field.name = name
        field.text = text
        field.is_default = is_default
        field.group_name_id = group_id
        db.session.commit()
        flash_for_fields('The field has been updated successfully!', 'success')
        return redirect(url_for('users_field.all_fields', group_id=group_id))
    return render_template('user_fields/update_fields.html', field=field, group_id=group_id)

@fields_blueprint.route('/groups/<int:group_id>/fields/<int:field_id>/delete_fields>', methods=['GET',"POST"])
def delete_fields(group_id,field_id):
    field = Field.query.get(field_id)
    if field:
        db.session.delete(field)
        db.session.commit()
        flash_for_fields('Field Deleted Successfully', 'success')
    else:
        flash_for_fields('Field not found', 'error')
    return redirect(url_for('users_field.all_fields',group_id=group_id,field_id=field_id))

@fields_blueprint.route('/groups/groups',methods=["GET","POST"])
def back_to_group():
    return redirect(url_for('users_group.groups'))
