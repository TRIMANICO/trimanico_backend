from rest_framework import serializers
from .models import User


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


class VerifyAccountSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField()
    


    

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']
