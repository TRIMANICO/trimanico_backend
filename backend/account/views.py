from django.shortcuts import render

# Create your views here.

from .renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import  UserRegistrationSerializer,UserLoginSerializer,VerifyAccountSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .emails import send_otp_via_email
from .models import User
#creating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
      #sets the data attribute with request.value 
      serializer=UserRegistrationSerializer(data=request.data)
      #check if any field is empty, runs validate() and set validate_data with user data
      serializer.is_valid(raise_exception=True)
         #returns the __str__ method of user model and .save() triggers the create method
      user=serializer.save()
      send_otp_via_email(serializer.data['email'])
      # token=get_tokens_for_user(user)
        # print(user)
        #  return Response({"data":serializer.validated_data})
      return Response({"msg":"verification code send. check email","data":serializer.data},status=status.HTTP_200_OK)
    
class VerifyOTP(APIView):
   def post(self,request):
      try:
         serializer=VerifyAccountSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         email=serializer.data["email"]
         otp=serializer.data["otp"]
         user=User.objects.filter(email=email)
         user=user.first()
         if not user:
            return Response({"msg":"Invalid email"},status=status.HTTP_400_BAD_REQUEST)
         if not user.otp==otp:
            return Response({"msg":"Invalid otp"},status=status.HTTP_400_BAD_REQUEST)
         user.is_verified=True
         user.save()
         return Response({"msg":"account verified"},status=status.HTTP_200_OK)
      except Exception as e:
         print(e)
      
   
   

class UserLoginView(APIView):
   renderer_classes=[UserRenderer]
   def post(self,request,format=None):
      serializer=UserLoginSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      email=serializer.data.get("email")
      password=serializer.data.get("password")
      user= User.objects.filter(email=email)
      user=user.first()
      if not user.is_verified:
         return Response({"errors":{'non_fields_errors':["user is not verified"]}},status=status.HTTP_200_OK)
      user=authenticate(email=email,password=password)
      if user is not None:
        token=get_tokens_for_user(user)
        return Response({"token":token,"msg":"login success"},status=status.HTTP_200_OK)
      else:
        return Response({"errors":{'non_fields_errors':["email or password is not valid"]}},status=status.HTTP_404_NOT_FOUND)





   