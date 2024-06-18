from django.urls import path
from .views import UserRegistrationView,UserLoginView,VerifyRegistrationOTPView,UserChangePasswordView,SendpasswordResetEmailView,UserPasswordResetView,VerifyPasswordResetOtpView
urlpatterns=[
     path('register/',UserRegistrationView.as_view(),name="register"),
     path('login/',UserLoginView.as_view(),name="login"),
     path('verify-register-otp/',VerifyRegistrationOTPView.as_view(),name="verify-otp"),
     path('verify-password-otp/',VerifyPasswordResetOtpView.as_view(),name="verify-password-otp"),
     path('changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
     path('send-reset-password-email/',SendpasswordResetEmailView.as_view(),name='send-reset-password-email'),
     path('reset-password/',UserPasswordResetView.as_view(),name="reset-password"),
]