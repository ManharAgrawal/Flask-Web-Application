import pdb
from config import db
from flask_login import current_user   
from sql_database.models import Field, GroupName
from flask import Blueprint, render_template, request, flash, url_for, redirect

fields_blueprint = Blueprint('users_field', __name__, template_folder='templates/user_fields')

@fields_blueprint.route('/all_fields', methods=["GET","POST"])
def all_fields():
    user = current_user
    groups = user.groups
    all_fields = []
    for group in groups:
        all_fields.extend(group.field)
    return render_template('user_fields/all_fields.html', fields=all_fields)

@fields_blueprint.route('/create_fields',methods=["GET","POST"])
def create_fields():
    if request.method=="POST":
        group_id = request.form.get('group')
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
        flash('Field Created Successfully!')
        return redirect(url_for('users_field.all_fields'))
    group = GroupName.query.all()
    context = {"groups":group}
    return render_template("user_fields/text_field.html",**context) 

@fields_blueprint.route('/update_fields/<int:id>', methods=["GET", "POST"])
def update_fields(id):
    if request.method=="POST":
        field = Field.query.filter_by(id=id).one()
        group_id = request.form.get('group')
        name = request.form.get('name')
        text = request.form.get('text')
        is_default = request.form.get('is_default')
        field.name = name
        field.text = text
        field.is_default = is_default
        field.group_name_id = group_id
        db.session.commit()
        flash('The group has been updated successfully!','success')
        return redirect(url_for('users_field.all_fields'))
    return render_template('user_fields_/update_fields.html')

@fields_blueprint.route('/delete_fields/<int:id>', methods=['GET',"POST"])
def delete_fields(id):
    field = Field.query.get(id)
    if field:
        db.session.delete(field)
        db.session.commit()
        flash('Field Deleted Successfully')
    else:
        flash('Field not found')
    return redirect(url_for('users_field.all_fields'))

@fields_blueprint.route('/groups',methods=["GET","POST"])
def back_to_group():
    return redirect(url_for('users_group.groups'))