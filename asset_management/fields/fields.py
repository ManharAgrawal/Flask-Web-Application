import pdb
from config import db
from sql_database.models import GroupName, Field
from flask import Blueprint, render_template, request, flash, url_for, redirect

fields_blueprint = Blueprint('fields', __name__, template_folder='templates/fields')

@fields_blueprint.route('/')
def all_fields():
    if request.method == "POST":
        group_id = request.form.get('group')
        name = request.form.get('name')
        text = request.form.get('type')
        is_default = request.form.get('is_default')
        if group_id:
            new_field = Field(name=name, text=text, is_default=is_default, group_name_id=group_id)
            db.session.add(new_field)
            db.session.commit()
            flash('Field field created successfully!')
            return redirect(url_for('all_fields'))
        else:
            flash('Field Not Found')
    field = Field.query.all()
    return render_template('all_fields.html', field=field)

@fields_blueprint.route('/group_fields', methods=["GET", "POST"])
def group_fields():
    groups = GroupName.query.all()
    return render_template('group_fields.html', groups=groups)

@fields_blueprint.route('/update_field/<int:id>', methods=["GET","POST"])
def update_field(id): 
    field = Field.query.get(id)
    if request.method == "POST":
        name = request.form.get('name')
        text = request.form.get('text')
        is_default = request.form.get('is_default')
        field.name = name
        field.text = text
        field.is_default = is_default
        db.session.add(field)
        db.session.commit()
        flash("Field updated successfully")
        return redirect(url_for('all_fields'))
    return render_template('group_fields.html',fields=field)

@fields_blueprint.route('/delete_field/<int:id>', methods=["GET","POST"])
def delete_field(id):
    field = Field.query.filter_by(id=id).first()
    if field:
        db.session.delete(field)
        db.session.commit()
        flash('Field Data Deleted Successfully')
        return redirect(url_for('all_fields'))
    else:
        flash('Field not found')
    return redirect(url_for('all_fields'))