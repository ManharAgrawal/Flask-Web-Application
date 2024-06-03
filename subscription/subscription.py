import time
from config import db, razorpay_client
from flask_login import login_required, current_user
from sql_database.models import User, GroupName
from flask import Blueprint, render_template, redirect, url_for, flash, request

subscription_blueprint = Blueprint('subscription', __name__, template_folder='templates/subscription')

PLAN_IDS = {
    'monthly': 0,
    'six_months': 1,
    'yearly': 2
}

# products - basic standered, interprice

SUBSCRIPTION_AMOUNTS = {
    'monthly': 10000,   # Amount in paisa (100.00 INR)
    'six_months': 50000,  # Amount in paisa (500.00 INR)
    'yearly': 100000     # Amount in paisa (1000.00 INR)
}

DURATION = {
    'monthly': 'monthly',
    'six_months': 'six_months',
    'yearly': 'yearly'
}

@subscription_blueprint.route('/subscription', methods=['GET', 'POST'])
def subscription():
    if request.method == 'POST':
        amount = SUBSCRIPTION_AMOUNTS.get(DURATION)
        try:
            subscription_data = {
                "plan_id": PLAN_IDS.get(DURATION),
                "total_count": 1,
                "customer_notify": 1,
                "addons": [],
                "notes": {"subscription_type": DURATION}
            }
            subscription = razorpay_client.subscription.create(data=subscription_data)
            return render_template('payment.html', subscription_id=subscription.get('id'), amount=amount)
        except Exception as e:
            return render_template('user_groups/groups.html', error=str(e))
    return render_template('subscription/sub.html')

@subscription_blueprint.route('/payment_callback', methods=["GET"])
def payment_callback():
    user = User.query.get(current_user.id)
    if user:
        user.subscription_status = 'active'
        db.session.commit()
        flash('Subscription activated successfully.', 'success')
    else:
        flash('Subscription activation failed.', 'error')

    return redirect(url_for('groups.group_page'))
