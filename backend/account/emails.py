from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User
def send_otp_via_email(email):
    try:
        subject="your account verification email"
        otp=random.randint(100000,999999)
        message= f' your otp is {otp}'
        email_from=settings.EMAIL_HOST_USER
        send_mail(subject,message,email_from,[email])
        user_obj=User.objects.get(email=email)
        user_obj.otp=otp
        user_obj.save()
    except Exception as e:
        print("error",e)



from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get("EMAIL_FROM"),
            to=[data['to_email']]
        )
        email.send()