# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomUserManager # Make sure CustomUserManager is imported if needed for display in admin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # The fields to be displayed in the list view of the admin
    list_display = ('email', 'is_verified', 'is_staff', 'is_active', 'date_joined')
    # The fields that can be used to filter the list
    list_filter = ('is_staff', 'is_active', 'is_verified')
    # The fields that can be searched
    search_fields = ('email',)
    # The order in which users are displayed
    ordering = ('email',)
    # Fieldsets for adding/changing a user in the admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('is_verified',)}), # Added is_verified here
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # Addfieldsets for adding a new user from the admin (if you wanted to add extra fields during creation)
    # We'll stick to a simpler form for now, as CustomUserAdmin inherits default UserAdmin forms
    # For simplicity, we'll use the default add_fieldsets from UserAdmin and just customize the main ones.
    # If you needed to remove username, you'd customize get_fieldsets or add_fieldsets method.

# If you remove the @admin.register(CustomUser) decorator:
# admin.site.register(CustomUser, CustomUserAdmin)