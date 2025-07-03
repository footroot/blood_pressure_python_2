# D:\blood_pressure\blood_pressure_python_2\users\admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Alias UserAdmin to avoid confusion
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin): # Inherit from BaseUserAdmin (aliased UserAdmin)
    # Forms to use for adding and changing users in the admin
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # The fields to be displayed in the list view of the admin
    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'is_active', 'date_joined')
    # The fields that can be used to filter the list
    list_filter = ('is_staff', 'is_active', 'is_verified')
    # The fields that can be searched
    search_fields = ('email', 'first_name', 'last_name') # Added first/last name to search
    # The order in which users are displayed
    ordering = ('email',)

    # === Completely Redefined Fieldsets for changing an existing user ===
    # This structure is necessary because your CustomUser is based on AbstractBaseUser,
    # which doesn't have the default fields (like username) that BaseUserAdmin's fieldsets assume.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal Info'), {'fields': ('first_name', 'last_name', 'address', 'phone_mobile', 'phone_landline', 'phone_emergency', 'profile_picture', 'is_verified')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # === Completely Redefined Add Fieldsets for adding a new user ===
    # This structure mirrors the fields in CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'), # password2 is for confirmation in the form
        }),
        (('Personal Information'), {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'address', 'phone_mobile', 'phone_landline', 'phone_emergency', 'profile_picture'),
        }),
        (('Permissions'), {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
    )