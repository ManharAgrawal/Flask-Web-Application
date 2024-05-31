import time
from config import razorpay_client
from flask_login import current_user
from decorators.decorators import login_required
from sql_database.models import Payment, db, User
from flask import Blueprint, render_template, request, redirect, url_for, flash

payment_blueprint = Blueprint('payment', __name__, template_folder='templates/payment')

@payment_blueprint.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        amount = request.form.get('amount')
        subscription = request.form.get('subscription')
        new_payment = Payment(name=name, email=email, amount=float(amount), subscription=subscription)
        db.session.add(new_payment)
        db.session.commit()
        response = razorpay_client.payment_link.create({
            "amount": int(float(amount) * 100),
            "currency": "INR",
            "description": "Subscription payment",
            "accept_partial": False,
            "customer": {
                "name": name,
                "email": email,
            },
            "notify": {
                "sms": False,
                "email": True
            },
            "callback_url": url_for("payment.payment_callback", payment_id=new_payment.id, _external=True),
            "callback_method": "get"
        })
        payment_link_url = response.get('short_url')
        if not payment_link_url:
            flash('Failed to generate payment link. Please try again.', 'error')
            return redirect(url_for("payment.payment"))
        new_payment.payment_link_url = payment_link_url
        db.session.commit()
        flash('Payment confirmed successfully!', 'success')
        return redirect(payment_link_url)
    
    return render_template('payment_form.html')

@payment_blueprint.route('/payment_callback/<int:payment_id>', methods=["GET"])
def payment_callback(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        flash("No payment found.", "error")
        return redirect(url_for("payment.payment"))
    if payment.payment_status == 'pending':
        payment.payment_status = 'paid'
        db.session.add(payment)
        db.session.commit()
        flash("Payment confirmed successfully.", "success")
    else:
        flash("Payment already confirmed.", "error")
    
    return redirect(url_for("payment.success"))

def create_razorpay_plan(name, interval):
    if interval == 'monthly':
        period = 'monthly'
        amount = 10000  # Example amount for monthly plan in paise (INR 100)
    elif interval == 'quarterly':
        period = '3 months'
        amount = 25000  # Example amount for quarterly plan in paise (INR 250)
    elif interval == 'annually':
        period = '1 year'
        amount = 100000  # Example amount for annual plan in paise (INR 1000)
    else:
        raise ValueError("Invalid interval")
    response = razorpay_client.plan.create({
        "period": period,
        "interval": 1,
        "item": {
            "name": name,
            "amount": amount,
            "currency": "INR",
            "interval": 1,
            "period": period,
        }
    })
    return response

@payment_blueprint.route('/subscribe_plan/<plan_id>', methods=['POST'])
@login_required
def subscribe_plan(plan_id):
    plan = Payment.query.filter_by(plan_id=plan_id).first()
    if not plan:
        flash('Plan not found!', 'error')
        return redirect(url_for('dashboard'))
    
    # Create a Razorpay subscription here
    subscription_response = razorpay_client.subscription.create({
        "plan_id": plan.plan_id,
        "customer_notify": 1,
        "total_count": 12,  # Number of billing cycles
        "start_at": int(time.time()) + 60,  # Start the subscription after 1 minute
        "addons": [{
            "item": {
                "name": plan.name,
                "amount": plan.amount,
                "currency": "INR"
            }
        }]
    })

    # Update user's group creation limit based on subscription plan
    user = User.query.filter_by(id=current_user.id).first()
    if user:
        if plan.subscription == 'monthly':
            user.group_limit += 50
        elif plan.subscription == 'quarterly':
            user.group_limit += 100
        elif plan.subscription == 'annually':
            user.group_limit += 500
        db.session.commit()

        flash('Subscribed successfully!', 'success')
    else:
        flash('User not found!', 'error')
    
    return redirect(url_for('dashboard'))
