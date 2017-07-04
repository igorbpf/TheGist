from news import get_summary, get_summary_text
from blue import celery, app, mail
from flask_mail import Message

import os

@celery.task
def summarize(url):
    title, summary, language = get_summary(url)


    # Send email to the adimin whe someone uses the Api
    message = "Someone is using the TheGist Api."
    send_email.apply_async(args=[message])

    return {'title': title, 'summary': summary}


@celery.task
def summarize_text(text, size):
    if size == 'Small':
        bit = 0.25
    elif size == 'Medium':
        bit = 0.50
    elif size == 'Big':
        bit = 0.75
    summary = get_summary_text(text, bit)

    # Send email to the adimin whe someone uses the Api
    message = "Someone is using the TheGist app."
    send_email.apply_async(args=[message])

    return {'summary': summary}


@celery.task
def send_email(message):
    '''Send an email everytime someone uses it'''
    recipient = [os.environ['RECIPIENT_MAIL']]
    header = 'Hello from TheGist'
    with app.app_context():
        msg = Message(header, recipients=recipient)
        msg.body = message
        mail.send(msg)
