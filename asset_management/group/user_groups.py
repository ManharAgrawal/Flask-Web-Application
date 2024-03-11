import pdb
from config import db
from flask_login import current_user
from sql_database.models import GroupName, Field
from flask import Blueprint, render_template, request, redirect, url_for, flash

groups_blueprint = Blueprint('users_group', __name__, template_folder='templates/user_groups')

@groups_blueprint.route('/groups', methods=["GET", "POST"])
def groups():
    if request.method == "POST":
        user_id = current_user.id
        name = request.form.get('name')
        description = request.form.get('description')
        status = request.form.get('status')
        if name and description and status: 
            new_group = GroupName(name=name, description=description, status=status, user_id=user_id)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created successfully!', 'success')
            return redirect(url_for('users_group.groups'))
    groups = GroupName.query.filter_by(user_id=current_user.id).all()
    return render_template("user_groups/groups.html", entities=groups)
    
@groups_blueprint.route('/groups/group_fields', methods=["GET", "POST"])
def group_fields():
    return render_template('user_groups/group_fields.html')

@groups_blueprint.route('/groups/<int:group_id>/update_groups>', methods=["GET", "POST"])
def update_groups(group_id):
    group = GroupName.query.get(group_id)
    if request.method=="POST":
        group.name = request.form['name']
        group.description = request.form['description']
        group.status = request.form['status']
        db.session.commit()
        flash('The group has been updated successfully!','success')
        return redirect(url_for('users_group.groups'))
    return render_template('user_groups/update_group.html', group=group)

@groups_blueprint.route('/groups/group_report', methods=["GET", "POST"])
def group_report():
    return render_template('user_groups/group_report.html')
    
@groups_blueprint.route('/groups/<int:group_id>/delete_groups', methods=["GET","POST"])
def delete_groups(group_id):
    group = GroupName.query.get(group_id)
    if group:
        Field.query.filter_by(group_id=group_id).delete()
        db.session.delete(group)
        db.session.commit()
        status_message, status = 'Group deleted succesfully !!!', 'success'
    else:
        status_message, status = 'Error in deleting group !!', 'error'
    flash(status_message, status)
    return redirect(url_for('users_group.groups', group_id=group_id))