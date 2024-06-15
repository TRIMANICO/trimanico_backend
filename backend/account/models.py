from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None,confirm_password=None,**extra_fields):
        if not email:
            raise ValueError("email is required")
        #converts email in lowercase 
        email=self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields  
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None,**extra_fields):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user 
       


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name=models.CharField(max_length=30)
    middle_name=models.CharField(max_length=30,null=True,blank=True)
    last_name=models.CharField(max_length=30)
    date_of_birth=models.DateField(null=True,blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=6,null=True,blank=True)
   

    created_at=models.DateTimeField(auto_now_add=True)
    

    #make usermanager model above user model
    objects=UserManager()

    #login through email
    USERNAME_FIELD = 'email'
    
    #email filed is automatically required
    REQUIRED_FIELDS = ["first_name",]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

    