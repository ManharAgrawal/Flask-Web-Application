import pdb
from config import db
from flask_login import current_user
from sql_database.models import GroupName
from flask import Blueprint, render_template, request, redirect, url_for,flash

groups_blueprint = Blueprint('groups', __name__, template_folder='templates/groups')

@groups_blueprint.route('/')
def groups():
    if request.method == "POST":
        # pdb.set_trace()
        user_id = current_user.id
        name = request.form.get('name')
        description = request.form.get('description')
        if user_id: 
            new_group = GroupName(name=name, description=description, user=user_id)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created successfully!')
            return redirect(url_for('groups'))
    groups = GroupName.query.filter_by(user=current_user.id)
    return render_template('groups/groups.html', entities=groups)

@groups_blueprint.route('/text_field',methods=["GET","POST"])    
def text_field():
    return render_template('text_field.html')

@groups_blueprint.route('/update_group/<int:id>',methods=["GET","POST"])
def update_group(id):
    group = GroupName.query.get(id)
    if request.method == "POST":
        id = request.form.get('id')
        name = request.form.get('name')
        description = request.form.get('description')
        if group:
            group.name = name
            group.description = description
            db.session.add(group)
            db.session.commit()
            flash("Group updated successfully")
            return redirect(url_for('groups'))
    return render_template('text_field.html',entity=group)

@groups_blueprint.route('/delete_group/<int:id>', methods=['GET',"POST"])
def delete_group(id):
    group = GroupName.query.filter_by(id=id).first()
    if group:
        db.session.delete(group)
        db.session.commit()
        flash('Group Data Deleted Successfully')
        return redirect(url_for('groups'))
    else:
        flash('Group not found')
    return redirect(url_for('groups'))
