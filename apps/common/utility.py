import re
import threading

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        print(f"this is thread data: {data}")
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        print(f"this is data args: \nsub: {data['subject']}\nbody: {data['body']}\nto email: {data['to_email']}\ndata con type: {data['context_type']}")
        if data.get('content_type') == 'html':
            email.content_subtype = 'html'
        EmailThread(email).start()


def send_mail(email, code):
    html_content = render_to_string(
        "email/authentication/activate_account.html",
        {"code": code}
    )
    Email.send_email(
        {
            'subject': "ro'yxatdan o'tish",
            'to_email': email,
            'body': html_content,
            'context_type': "html"
        }
    )