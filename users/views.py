from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView # For signup and potentialy a home page
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

# Create your views here.

# --Home Page View--
class HomePageView(TemplateView):
    template_name = 'users/home.html'

# ---User Registration View---
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page after successful signup
    template_name = 'users/signup.html'    

    def form_valid(self, form):
        response = super().form_valid(form)
        # Send verification email (to implement later)
        messages.success(self.request, 'Your account has been created successfully! Please check your email to verify your account')
        return response

# ---User Login View---
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True # Redirect logged in users from login page

    def get_success_url(self):
        #Customize where to go after login
        return reverse_lazy('home') # Redirect to home page
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)

# ---User Logout View---
# Django's LogoutView handles most of the logic.
# We just need to define a success_url and optionally add a message.
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login') #Redirect to login after logout

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'You have been logged out successfully.')
        return response