from config import mail
from flask_mail import Message
from flask import request
import pdb

def send_email(subject, recipient, body):
    try:
        pdb.set_trace()
        email = request.form.get('email')
        recipient = 'manhar@webkorps.com'
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