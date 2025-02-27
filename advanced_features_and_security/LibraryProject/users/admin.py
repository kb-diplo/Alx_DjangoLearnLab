# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser model"""
    model = CustomUser
    
    # Add the new fields to various admin views
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    list_display = UserAdmin.list_display + ('date_of_birth',)
    search_fields = UserAdmin.search_fields + ('date_of_birth',)

# Register the model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)