import pdb
from config import db
from datetime import datetime
from flask_login import current_user
from sql_database.models import GroupName, Field
from flask import Blueprint, render_template, request, redirect, url_for, flash

groups_blueprint = Blueprint('users_group', __name__, template_folder='templates/user_groups')

@groups_blueprint.route('/groups', methods=["GET"])
def group_page():
    user_groups = GroupName.query.filter_by(user_id=current_user.id).all()
    return render_template("user_groups/groups.html", entities=user_groups)

@groups_blueprint.route('/groups', methods=["POST"])
def groups():
    user_id = current_user.id
    name = request.form.get('name')
    description = request.form.get('description')
    created_date = datetime.utcnow()
    updated_date = datetime.utcnow()
    if not name:
        status_message, status = "Name field is required", "error"
        return redirect(url_for("users_group.create"))
    existing_group = GroupName.query.filter_by(name=name).first()
    if existing_group:
        flash("A group with the same name already exists", "error")
        return redirect(url_for("users_group.create"))
    new_group = GroupName(name=name, description=description, user_id=user_id, created_date=created_date, updated_date=updated_date)
    db.session.add(new_group)
    db.session.commit()
    status_message, status = 'Group created successfully!', 'success'
    flash(status_message, status)
    return redirect(url_for("users_group.groups", entities=groups))

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
    group.name = request.form.get('name')
    group.description = request.form.get('description')
    group.updated_data = datetime.utcnow()
    db.session.commit()
    flash('The group has been updated successfully!','success')
    return redirect(url_for('users_group.groups'))

@groups_blueprint.route('/groups/<int:id>/delete')
def delete(id):
    group = GroupName.query.get(id)
    if group:
        fields = Field.query.filter_by(group_id=id).all()
        deleted_data = {'group': group, 'fields': fields}
        try:
            Field.query.filter_by(group_id=id).delete()
            db.session.delete(group)
            db.session.commit()
            status_message, status = 'Group Deleted Successfully!!!', 'success'
        except Exception as e:
            db.session.rollback()
            db.session.add(deleted_data['group'])
            db.session.add_all(deleted_data['fields'])
            db.session.commit()
            status_message, status = 'Error In Deleting Group', 'error'
    flash(status_message, status)
    return redirect(url_for('users_group.groups', id=id))