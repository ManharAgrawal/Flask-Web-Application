import pdb
from config import mail
from flask import request
from flask_mail import Message
from flask_login import current_user 

def send_email(subject, recipient, body, html_body=None):
    try:
        email = request.form.get('email')
        recipient = current_user.email
        msg = Message(
            subject,
            sender = 'your_email_address',
            recipients = [recipient]
        )
        msg.body = body
        if html_body:
            msg.html = html_body
        mail.send(msg)
        return True   
    except Exception as e:
        print("Error sending email:", e)
        return False