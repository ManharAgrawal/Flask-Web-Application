import pdb
from config import mail
from flask import request
from flask_mail import Message
from flask_login import current_user 

def send_email(subject, recipient, body):
    try:
        email = request.form.get('email')
        recipient = current_user.email
        msg = Message(
            subject,
            sender = 'manharagrawal19@gmail.com',
            recipients = [recipient]
        )
        msg.body = body
        mail.send(msg)
        return True   
    except Exception as e:
        print("Error sending email:", e)
        return False