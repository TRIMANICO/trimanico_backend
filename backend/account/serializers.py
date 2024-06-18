from rest_framework import serializers
from .models import User

class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)


class UserRegistrationSerializer(serializers.ModelSerializer):
    # we are writing this because we need to confirm password filed in our registration request
    #this doesnot include the password2 in response object
    confirm_password=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields="__all__"
        extra_kwargs={
            'password':{'write_only':True}
        }
    #validating password and confirm password while registration
  # this function runs when is_valid method is called on instance of UserRegistrationSerializer
    def validate(self, attrs):
        # print(attrs)
        password=attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        if password!=confirm_password:
            raise serializers.ValidationError("password and confirm password doenot match")
        return attrs
    def create(self,data):
        #the data contains the validate_data data
       # print(data)
        return User.objects.create_user(**data)


class VerifyOtpSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField()
    


    

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']


class UserChangePasswordSerializer(serializers.Serializer):
    prev_password=serializers.CharField(max_length=255,style={"input_type:password"},write_only=True)
    new_password=serializers.CharField(max_length=255,style={"input_type":"password"},write_only=True)
    confirm_password=serializers.CharField(max_length=255,style={"input_type":"password"},write_only=True)
    class Meta:
        fields=["new_password","confirm_password","prev_password"]
    def validate(self, attrs):
        new_password=attrs.get("new_password")
        confirm_password=attrs.get("confirm_password")
        prev_password=attrs.get('prev_password')
        #is the way to extract data passed in context
        user=self.context.get("user")
        if not user.check_password(prev_password):
            raise serializers.ValidationError("Incorrect previous password.")
        if(new_password!=confirm_password):
            raise serializers.ValidationError("password and confirm password doenot match")
        user.set_password(new_password)
        user.save()
        return attrs
       

class SendpasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    

class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={"input_type":"password"},write_only=True)
    confirm_password=serializers.CharField(max_length=255,style={"input_type":"password"},write_only=True)
    class Meta:
        fields=["password","confirm_password"]
    def validate(self, attrs):
            password=attrs.get("password")
            confirm_password=attrs.get("confirm_password")
            if(password!=confirm_password):
                raise serializers.ValidationError("password and confirm password doenot match")
            return attrs
       


