from django.urls import path
from .views import UserRegistrationView,GenerateOtp,VerifyOtpView,UserLoginView,VerifyRegistrationOTP,UserChangePasswordView,SendpasswordResetEmailView,UserPasswordResetView
urlpatterns=[
     path('register/',UserRegistrationView.as_view(),name="register"),
     path('login/',UserLoginView.as_view(),name="login"),
     path('verify-otp/',VerifyRegistrationOTP.as_view(),name="verify-otp"),
     path('generate/',GenerateOtp.as_view()),
     path('veri/',VerifyOtpView.as_view()),
     path('changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
     path('send-reset-password-email/',SendpasswordResetEmailView.as_view(),name='send-reset-password-email'),
     path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="reset-password"),
]