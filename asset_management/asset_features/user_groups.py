import pdb
from config import db
from flask_login import current_user, login_user
from sql_database.models import GroupName
from flask import Blueprint, render_template, request, redirect, url_for,flash

groups_blueprint = Blueprint('users_group', __name__, template_folder='templates/user_groups')

@groups_blueprint.route('/groups', methods=["GET","POST"])
def groups():
    if request.method == "POST":
        user_id = current_user.id
        name = request.form.get('name')
        description = request.form.get('description')
        if user_id: 
            new_group = GroupName(name=name, description=description, user=user_id)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created successfully!')
            return redirect(url_for('users_group.groups'))
    groups = GroupName.query.filter_by(user=current_user.id)
    return render_template('user_groups/groups.html', entities=groups)

@groups_blueprint.route('/group_fields', methods=["GET", "POST"])
def group_fields():
    return render_template('user_groups/group_fields.html')

@groups_blueprint.route('/update_fields/<int:id>',methods=["GET","POST"])
def update_fields(id):
    group = GroupName.query.get(id)
    if request.method == "POST":
        id = request.form.get('id')
        name = request.form.get('name')
        description = request.form.get('description')
        if group:
            group.name = name
            group.description = description
            db.session.commit()
            flash("Group Updated Successfully")
            return redirect(url_for('user_groups/groups_fields'))
    return render_template('user_groups/groups.html',group=group)

@groups_blueprint.route('/delete_groups/<int:id>', methods=["GET","POST"])
def delete_groups(id):
    group = GroupName.query.get(id)
    if group:
        db.session.delete(group)
        db.session.commit()
        flash('Group Data Deleted Successfully')
        return redirect(url_for('user_groups/groups'))
    else:
        flash('Group Not Found')
    return redirect(url_for('user_groups/groups'))
