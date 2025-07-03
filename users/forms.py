# D:\blood_pressure\blood_pressure_python_2\users\forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm # Import UserChangeForm for CustomUserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # These fields are required for initial signup based on your request.
    # We are explicitly adding them here because CustomUser is based on AbstractBaseUser,
    # which does not include first_name/last_name by default.
    first_name = forms.CharField(label='First name', max_length=150, required=True)
    last_name = forms.CharField(label='Last name', max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Fields to include in the registration form
        # 'email' is USERNAME_FIELD, so it's always implied for UserCreationForm's initial fields
        fields = (
            'email',
            'first_name',
            'last_name',
            'address',
            'phone_mobile',
            'phone_landline',
            'phone_emergency',
            'profile_picture',
        )

# This form is for the Django Admin interface to change a user
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        # Include all fields from CustomUser for the admin interface,
        # plus standard AbstractBaseUser fields like password
        fields = (
            'email',
            'first_name',
            'last_name',
            'address',
            'phone_mobile',
            'phone_landline',
            'phone_emergency',
            'profile_picture',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_verified', # Your custom verification field
            'groups',
            'user_permissions',
            'last_login',
            'date_joined',
        )

# This form is for users to update their own profile information via a web page
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'address',
            'phone_mobile',
            'phone_landline',
            'phone_emergency',
            'profile_picture',
        )
        # You can add widgets for better UI if needed, e.g.:
        # widgets = {
        #     'address': forms.Textarea(attrs={'rows': 3}),
        # }


class CustomAuthenticationForm(AuthenticationForm):
    # This form is for logging in, where username is changed to email
    username = forms.EmailField(label="Email") # Change 'username' label to 'Email'