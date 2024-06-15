from django.urls import path
from .views import UserRegistrationView,UserLoginView,VerifyOTP,UserChangePasswordView,SendpasswordResetEmailView,UserPasswordResetView
urlpatterns=[
     path('register/',UserRegistrationView.as_view(),name="register"),
     path('login/',UserLoginView.as_view(),name="login"),
     path('verify-otp/',VerifyOTP.as_view(),name="verify-otp"),
     path('changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
     path('send-reset-password-email/',SendpasswordResetEmailView.as_view(),name='send-reset-password-email'),
     path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="reset-password"),
]