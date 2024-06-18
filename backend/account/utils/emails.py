from django.core.mail import send_mail
from django.conf import settings
def send_otp_via_email(email,otp):
    subject="your account verification email"
    message= f'your otp is {otp}'
    email_from=settings.EMAIL_HOST_USER
    try:
        send_mail(subject,message,email_from,[email])
        return True
    except Exception as e:
        print("error",e)
        return False
    



