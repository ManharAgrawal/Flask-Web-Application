import pdb
from config import db
from datetime import datetime
from flask_login import current_user
from notifications.notifications import send_email
from sql_database.models import GroupName, Field, User
from decorators.decorators import for_database, login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash

groups_blueprint = Blueprint('users_group', __name__, template_folder='templates/user_groups')

@groups_blueprint.route('/groups', methods=["GET"])
@login_required
@for_database
def group_page():
    user_groups = GroupName.query.filter_by(user_id=current_user.id).all()
    return render_template("user_groups/groups.html", entities=user_groups)

@groups_blueprint.route('/groups/create', methods=["GET"])
@login_required
def create():
    return render_template('user_groups/create.html')

@groups_blueprint.route('/groups', methods=["POST"])
def groups():
    user_id = current_user.id
    name = request.form.get('name')
    description = request.form.get('description')
    created_date = datetime.utcnow() # deprecated - no longer mention
    updated_date = datetime.utcnow()
    payment_status = request.form.get('payment_status')
    plan_id = request.form.get('plan_id')
    subscription = request.form.get('subscription')
    if not name:
        message_status, status = "Name field is required", "error"
        return redirect(url_for("users_group.create"))
    existing_group = GroupName.query.filter_by(name=name).first()
    if existing_group:
        message_status, status = "A group with the same name already exists", "error"
        return redirect(url_for("users_group.create"))
    new_group = GroupName(name=name, description=description, user_id=user_id, created_date=created_date, updated_date=updated_date,payment_status=payment_status,plan_id=plan_id,subscription=subscription)
    db.session.add(new_group)
    db.session.commit()
    group = GroupName.query.filter_by(name=name).first()
    user = User.query.get(group.user_id)
    subject = "New Group Created"
    body = f"Dear {user.name},\n\nA New Group '{group.name}' has been created.\n\nGroup Description: {group.description}\n\nGroup Created By: {user.name}\n\nGroup Created Date: {group.created_date}\n\nBest regards,\nThe App Team"
    html_body = render_template('user_groups/group_create.html', user=user, group=group)
    send_email(subject, user.email, body, html_body)
    message_status, status = 'Group created successfully and payment confirmed!', 'success'
    flash(message_status, status)
    return redirect(url_for('subscription.subscribe'))

@groups_blueprint.route('/groups/<int:id>/update', methods=["GET"])
@login_required
def update_page(id):
    group = GroupName.query.get(id)
    return render_template('user_groups/update.html', group=group)

@groups_blueprint.route('/groups/<int:id>/update', methods=["POST"])
def update(id):
    group = GroupName.query.get(id)
    old_name = group.name
    old_description = group.description
    group.name = request.form.get('name')
    group.description = request.form.get('description')
    group.updated_data = datetime.utcnow()
    db.session.commit()
    user = User.query.get(current_user.id)
    subject = "Group Updated"
    body = f"Dear {user.name},\n\nThe Group '{old_name}' has been updated.\n\nOld Group Name: {old_name}\nOld Group Description: {old_description}\n\nNew Name: {group.name}\nNew Description: {group.description}\n\nUpdated By: {user.name}\nGroup Updated Date: {group.updated_date}\n\nBest regards,\nThe App Team"
    html_body = render_template('user_groups/group_update.html', user=user, old_name=old_name, old_description=old_description, group=group)
    send_email(subject, user.email, body, html_body)
    flash('The Group has been Updated Successfully!','success')
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
    return redirect(url_for('users_group.groups'))