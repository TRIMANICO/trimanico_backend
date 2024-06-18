from django.urls import reverse
from .renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import  UserRegistrationSerializer,UserLoginSerializer,VerifyOtpSerializer,UserChangePasswordSerializer,VerifyOtpSerializer,SendpasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.utils.emails import send_otp_via_email
from .models import User,OTP,PasswordResetToken
from  account.utils.otp import verify_otp,generate_otp
from account.utils.rsa_utils import encrypt_message,decrypt_message
from account.utils.load_keys import load_public_key,load_private_key




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




class VerifyRegistrationOTPView(APIView):
   renderer_classes=[UserRenderer]
   def post(self,request):
         serializer=VerifyOtpSerializer(data=request.data)
         if serializer.is_valid(raise_exception=True):
            email=serializer.data["email"]
            otp=serializer.data["otp"]
            try:
               user = User.objects.get(email=email)
               if verify_otp(user, otp):
                  user.is_verified = True
                  user.save()
                  otp=OTP.objects.filter(user=user,otp_code=otp,used=False).latest('generated_at')
                  otp.used=True
                  otp.save()
                  return Response({"msg": "OTP verified successfully done"}, status=status.HTTP_200_OK)
               else:
                  return Response({"errors": {'otp_code': ["Invalid or expired OTP"]}}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"errors": {'email': ["User not found"]}}, status=status.HTTP_400_BAD_REQUEST) 
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
      serializer=UserChangePasswordSerializer(data=request.data,context={"user":request.user,"email":request.user.email})
      if serializer.is_valid(raise_exception=True):
         return Response({"msg":"password change successful"},status=status.HTTP_200_OK)
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendpasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendpasswordResetEmailSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
                otp = generate_otp(user)
                try:
                    send_otp_via_email(email, otp.otp_code)
                    return Response({"msg": "otp send successfully. Please check your email."}, status=status.HTTP_200_OK)
                except Exception:
                    return Response({"errors": {"non_field_errors": ["Could not send OTP."]}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except User.DoesNotExist:
                return Response({"errors": {"non_field_errors": ["User does not exist."]}}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyPasswordResetOtpView(APIView):
   renderer_classes=[UserRenderer]
   def post(self,request,format=None):
      serializer=VerifyOtpSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         otp=serializer.validated_data.get('otp')
         try:
            user=User.objects.get(email=serializer.validated_data.get('email'))
            if verify_otp(user,otp):
               print(user.id)
               print(type(user.id))
               encrypted_token = encrypt_message(str(user.id), load_public_key())
               print(type(encrypted_token))
               PasswordResetToken.objects.create(user=user, token=encrypted_token)
               return Response({"message": "OTP is valid.", "token": encrypted_token}, status=status.HTTP_200_OK)
            else:
               return Response({"errors":{"otp":["invalid otp"]}})
         except User.DoesNotExist:
            return Response({"errors": {"non_field_errors": ["User does not exist."]}}, status=status.HTTP_404_NOT_FOUND)   
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserPasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            password = serializer.validated_data['password']
            encrypted_token = request.data.get('token')
            print(encrypted_token)
            print(type(encrypted_token))
            
            try:
                # Decode the token from base64
                decoded_token = decrypt_message(encrypted_token,load_private_key())
                user = User.objects.get(id=int(decoded_token))
               #  print(type(decoded_token))
               #  print(decoded_token)
                token_record = PasswordResetToken.objects.get(user=user, token=encrypted_token)
                print(token_record)
                if token_record:
                   user.set_password(password)
                   user.save()
                   token_record.delete()  # Optionally delete the token after use
                   return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
                else:
                   return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({"error": "Invalid token format."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            except token_record.DoesNotExist:
                return Response({"error":"Token_record doesnot exist"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
                
            

           
               
               
              
           
        
   




