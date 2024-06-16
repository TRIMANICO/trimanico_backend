from django.urls import reverse
from .renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import  UserRegistrationSerializer,UserLoginSerializer,VerifyRegistrationOtpSerializer,UserChangePasswordSerializer,VerifyOtpSerializer,SendpasswordResetEmailSerializer,UserPasswordResetSerializer,OtpSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .emails import send_otp_via_email
from .models import User,OTP
from .utils import verify_otp,generate_otp



# Create your views here.


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
      #is_valid triggers validate method
      if serializer.is_valid(raise_exception=True):
         #.save() triggers create method
         user=serializer.save()
         otp=generate_otp(user)
         if send_otp_via_email(serializer.data['email'],otp) :
            verification_url = reverse('verify-otp')
            return Response({"msg":"verification code send. check email","redirect_url": verification_url},status=status.HTTP_200_OK)
         else:
            return Response({"errors":{"msg": ["User registered, but OTP email sending failed."]}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class VerifyRegistrationOTP(APIView):
   renderer_classes=[UserRenderer]
   def post(self,request):
         serializer=VerifyRegistrationOtpSerializer(data=request.data)
         if serializer.is_valid(raise_exception=True):
            email=serializer.data["email"]
            otp=serializer.data["otp"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"errors": {'email': ["User not found"]}}, status=status.HTTP_400_BAD_REQUEST)
            if verify_otp(user, otp):
                user.is_verified = True
                user.save()
                return Response({"msg": "OTP verified successfully done"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {'otp_code': ["Invalid or expired OTP"]}}, status=status.HTTP_400_BAD_REQUEST)
         else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
   renderer_classes=[UserRenderer]
   def post(self,request,format=None):
      serializer=UserLoginSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         email=serializer.data.get("email")
         password=serializer.data.get("password")
         user=authenticate(email=email,password=password)
         if user is  None:
            return Response({"errors":{'non_fields_errors':["email or password is not valid"]}},status=status.HTTP_404_NOT_FOUND)
         if not user.is_verified:
            return Response({"errors":{'non_fields_errors':["user is not verified"]}},status=status.HTTP_200_OK)
         token=get_tokens_for_user(user)
         return Response({"token":token,"msg":"login success"},status=status.HTTP_200_OK)
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
      

class UserChangePasswordView(APIView):
   renderer_classes=[UserRenderer]
   #user must be authenticated to change password
   permission_classes=[IsAuthenticated]
   def post(self,request,format=None):
      #context is used to serialize extra data and should be a dictionary
      serializer=UserChangePasswordSerializer(data=request.data,context={"user":request.user})
      if serializer.is_valid(raise_exception=True):
         return Response({"msg":"password change successful"},status=status.HTTP_200_OK)
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendpasswordResetEmailView(APIView):
   renderer_classes=[UserRenderer]
   def post(self,request,format=None):
      serializer=SendpasswordResetEmailSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         return Response({"msg":"password reset link send. Please check your email" , },status=status.HTTP_200_OK)
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
      


class UserPasswordResetView(APIView):
   renderer_classes=[UserRenderer]
   #uid and token are taken from url
   def post(self,request,uid,token,format=None):
      serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'Password Reset Successfully',},status=status.HTTP_200_OK)
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   




class GenerateOtp(APIView):
    def post(self, request, format=None):
        serializer=OtpSerializer(request.data)
        email=serializer.data.get('email')        
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        otp = generate_otp(user)
        send_otp_via_email(serializer.data['email'],otp.otp_code) 

        # Assuming you have a function to send OTP via email
        # send_otp_via_email(user.email, otp.otp_code)
        
        return Response({"msg": "OTP generated and sent to email", "otp_code": otp.otp_code}, status=status.HTTP_200_OK)
class VerifyOtpView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"errors": {'email': ["User not found"]}}, status=status.HTTP_400_BAD_REQUEST)
            
            if verify_otp(user, otp_code):
                user.is_verified = True
                user.save()
                return Response({"msg": "OTP verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {'otp_code': ["Invalid or expired OTP"]}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
