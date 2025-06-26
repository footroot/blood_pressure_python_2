from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',) #Only email is required for registration

        class CustomAuthenticationForm(AuthenticationForm):
            username = forms.EmailField(label='Email') # Change 'username' label to 'Email'