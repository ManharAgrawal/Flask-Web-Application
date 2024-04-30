import pdb
from config import db
from datetime import datetime
from flask_login import current_user
from sql_database.models import GroupName, Field
from flask import Blueprint, render_template, request, redirect, url_for, flash

status_blueprint = Blueprint('groups_status', __name__, template_folder='templates/group_status')

@status_blueprint.route('/status', methods=["GET"])
def status():
    return render_template('group_status/status.html')

@status_blueprint.route('/group', methods=["GET"])
def group():
    return render_template("users_group.group")