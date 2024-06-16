from django.contrib import admin
from .models import User,OTP
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


class UserAdmin(BaseUserAdmin):
    list_display = ["email", "first_name",'phone_number', "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name","middle_name","last_name","gender","address","phone_number"]}),
        ("Permissions", {"fields": ["is_admin","is_active","is_verified"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name","middle_name","last_name","gender","phone_number" ,"address","date_of_birth","password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(User,UserAdmin)
admin.site.register(OTP)