from flask import flash, redirect, request, url_for

def flash_for_users(message, category):
    flash(message, category)
    return redirect(url_for('users_group.groups'))

def flash_for_groups(message, category):
    flash(message, category)
    return redirect(url_for('users_group.groups'))

def flash_for_fields(message, category):
    flash(message, category)
    return redirect(url_for('users_group.groups'))
