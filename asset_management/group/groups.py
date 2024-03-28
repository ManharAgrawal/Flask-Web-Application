import pdb
from config import db
from flask_login import current_user
from sql_database.models import GroupName, Field
from flask import Blueprint, render_template, request, redirect, url_for, flash

groups_blueprint = Blueprint('users_group', __name__, template_folder='templates/user_groups')

@groups_blueprint.route('/groups', methods=["GET"])
def group_page():
    user_id = current_user.id
    user_groups = GroupName.query.filter_by(user_id=user_id).all()
    return render_template("user_groups/groups.html", entities=user_groups)

@groups_blueprint.route('/groups', methods=["POST"])
def groups():
    groups = GroupName.query.all()
    user_id = current_user.id
    name = request.form.get('name')
    description = request.form.get('description')
    if name: 
        new_group = GroupName(name=name, description=description, user_id=user_id)
        db.session.add(new_group)
        db.session.commit()
        status_message, message = 'Group created successfully!', 'success'
    else:
        status_message, message = "Enter Name", "error"
        flash(status_message,message)
        return redirect(url_for('users_group.groups'))
    return render_template("user_groups/groups.html", entities=groups)

@groups_blueprint.route('/groups/create', methods=["GET"])
def create():
    return render_template('user_groups/create.html')

@groups_blueprint.route('/groups/<int:id>/update', methods=["GET"])
def update_page(id):
    group = GroupName.query.get(id)
    return render_template('user_groups/update.html', group=group)

@groups_blueprint.route('/groups/<int:id>/update', methods=["POST"])
def update(id):
    group = GroupName.query.get(id)
    group.name = request.form['name']
    group.description = request.form['description']
    db.session.commit()
    flash('The group has been updated successfully!','success')
    return redirect(url_for('users_group.groups'))

@groups_blueprint.route('/groups/<int:id>/delete')
def delete(id):
    group = GroupName.query.get(id)
    if group:
        Field.query.filter_by(id=id).delete()
        db.session.delete(group)
        db.session.commit()
        status_message, status = 'Group deleted succesfully !!!', 'success'
    else:
        status_message, status = 'Error in deleting group !!', 'error'
    flash(status_message, status)
    return redirect(url_for('users_group.groups', id=id))