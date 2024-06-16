from django.core.mail import send_mail
from django.conf import settings
def send_otp_via_email(email,otp):
    subject="your account verification email"
    message= f'your otp is {otp}'
    email_from=settings.EMAIL_HOST_USER
    try:
        send_mail(subject,message,email_from,[email])
        print("send")
        return True
    except Exception as e:
        print("error",e)
        return False
    



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