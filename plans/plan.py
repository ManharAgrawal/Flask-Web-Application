import pdb
from flask_login import current_user
from config import db, razorpay_client
from sql_database.models import Plan, User
from flask import flash, redirect, url_for, Blueprint, render_template, request

plan_blueprint = Blueprint('plan', __name__, template_folder='templates/plans')

@plan_blueprint.route('/plans', methods=["GET"])
def plans():
    plans = Plan.query.all()
    return render_template('plans/plan.html', plans=plans)

@plan_blueprint.route('/create_plans', methods=["POST"])
def create_plans():
    try:
        # card no. - 4384113597424307
        # 1st otp - (In Phone)
        # 2nd otp no. - 267052 
        plan_id = request.form.get('plan_id')
        plan = Plan.query.get(plan_id)
        if not plan:
            message_status, status ='Plan not found!', 'error'
            return redirect(url_for('plan.plans'))
        callback_url = url_for('plan.payment_callback', _external=True)
        subscription_data = {
            "plan_id": plan.plan_id,
            "total_count": 1,
            "quantity": 1,
            "customer_notify": 1,
            "notify_info": {"notify_email": current_user.email},
            # "callback_url": callback_url
        }
        subscription = razorpay_client.subscription.create(subscription_data)
        payment_link = subscription['short_url']
        user = User.query.get(current_user.id)
        if user:
            user.subscription_status = 'active'
            user.subscription_id = subscription['id']
            db.session.commit()
            message_status, status ='Subscription activated successfully.', 'success'
        else:
            message_status, status ='Subscription activation failed.', 'error'
        return redirect(payment_link)
    except Exception as e:
        db.session.rollback()
        message_status, status = f"An error occurred: {str(e)}", "error"
    flash(message_status, status)    
    return redirect(url_for("plan.plans"))
    
@plan_blueprint.route('/payment_callback', methods=["GET"])
def payment_callback():
    user = User.query.get(current_user.id)
    if user:
        user.subscription_status = 'active'
        db.session.commit()
        flash('Subscription activated successfully.', 'success')
        return redirect(url_for('users_group.groups'))
    else:
        flash('Subscription activation failed.', 'error')
    return redirect(url_for('plan.plans'))