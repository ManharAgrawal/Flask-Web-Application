import pdb
from config import db
from sql_database.models import Field
from flask import Blueprint, render_template, request, flash, url_for, redirect

fields_blueprint = Blueprint('fields', __name__, template_folder='templates/user_fields')

@fields_blueprint.route('/all_fields', methods=["GET","POST"])
def all_fields():
    if request.method == "POST":
        group_id = request.form.get('group')
        name = request.form.get('name')
        text = request.form.get('text')
        is_default = request.form.get('is_default')
        if group_id:
            new_field = Field(name=name, text=text, is_default=is_default, group_name_id=group_id)
            db.session.add(new_field)
            db.session.commit()
            flash('Field Created Successfully!')
            return redirect(url_for('user_fields/all_fields'))
        else:
            flash('Field Not Found')
    field = Field.query.all()
    return render_template('user_fields/all_fields.html', field=field)

@fields_blueprint.route('/text_field',methods=["GET","POST"])    
def text_field():
    return render_template('user_fields/text_field.html')

@fields_blueprint.route('/update_groups/<int:id>', methods=["GET","POST"])
def update_groups(id): 
    field = Field.query.get(id)
    if request.method == "POST":
        name = request.form.get('name')
        text = request.form.get('text')
        is_default = request.form.get('is_default')
        field.name = name
        field.text = text
        field.is_default = is_default
        # db.session.add(field)
        db.session.commit()
        flash("Field updated successfully!")
        return redirect(url_for('user_fields/all_fields'))
    return render_template('user_fields/all_fields.html',groups=field)


@fields_blueprint.route('/groups',methods=["GET","POST"])
def back_to_group():
    return redirect(url_for('user_groups/groups'))

@fields_blueprint.route('/delete_fields/<int:id>', methods=['GET',"POST"])
def delete_fields(id):
    field = Field.query.get(id)
    if field:
        db.session.delete(field)
        db.session.commit()
        flash('Field Deleted Successfully')
        return redirect(url_for('user_fields/all_fields'))
    else:
        flash('Field not found')
    return redirect(url_for('user_fields/all_fields'))