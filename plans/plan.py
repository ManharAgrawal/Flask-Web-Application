import pdb
from flask_login import current_user
from config import db, razorpay_client
from sql_database.models import User
from flask import flash, redirect, url_for, Blueprint, render_template, request

plan_blueprint = Blueprint('plan', __name__, template_folder='templates/plans')

@plan_blueprint.route('/plans', methods=["GET"])
def plans():
    plans = razorpay_client.plan.all()
    return render_template('plans/plan.html', plans=plans["items"])

@plan_blueprint.route('/create_plans', methods=["POST"])
def create_plans():
    try:
        plan_id = request.form.get('plan_id')
        if not plan_id:
            message_status, status ='Plan not found!', 'error'
            return redirect(url_for('plan.plans'))
        subscription_data = {
            "plan_id": plan_id,
            "total_count": 1,
            "quantity": 1,
            "customer_notify": 1,
            "notify_info": {"notify_info":current_user.email},
        }
        subscription = razorpay_client.subscription.create(subscription_data)
        payment_link = subscription['short_url']
        user = User.query.get(current_user.id)
        if user:
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


@plan_blueprint.route('/expired_plan', methods=["GET"])
def expired_plan():
    return render_template('plans/expired_plan.html')