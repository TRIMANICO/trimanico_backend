import random
from django.utils import timezone
from account.models import OTP

def generate_otp(user):
    otp_code = str(random.randint(100000, 999999))
    print(otp_code)  # Generate a 6-digit OTP
    otp = OTP.objects.create(
        user=user,
        otp_code=otp_code,
        generated_at=timezone.now()
    )
    return otp

def verify_otp(user, otp_code):
    try:
        otp = OTP.objects.filter(user=user, otp_code=otp_code, used=False).latest('generated_at')
    except OTP.DoesNotExist:
        return False
    
    if otp.is_expired():
        return False

 
  
    otp.save()
    return True
