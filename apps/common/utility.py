from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string


def send_email(user, code, to_email):
    email_subject = "User tasdiqlash kodi emailingizga yuborildi"
    message = render_to_string('email/authentication/activate_account.html', {
            'user': user,
            'code': code,
            'uid': urlsafe_base64_encode(force_bytes(user.id))
        }
    )
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()

def send_reset_email(to_email, reset_link):
    subject= "sizning tasdiqlash havolangiz"
    message = f"link ustiga bosib o'zingizni tasdqlang va parolingizni o'zgartirng: \n{reset_link}"

    email = EmailMessage(subject, message, to=[to_email])
    email.send()