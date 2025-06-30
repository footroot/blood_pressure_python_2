from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
# For signup and potentialy a home page
from django.views.generic import CreateView, TemplateView, View
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

# For email verification
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six  # For Python 2/3 compatibility in tokens.py, used by Django's default PasswordResetTokenGenerator


# Create your views here.

# Helper class for token generation (Django's default for password reset)
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # We add is_verified to the hash to invalidate old tokens if user changes verification status
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active) + six.text_type(user.is_verified)
        )


account_activation_token = AccountActivationTokenGenerator()

# --Home Page View--


class HomePageView(TemplateView):
    template_name = 'users/home.html'

# ---User Registration View---


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account until email verification
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Activate Your Blood Pressure Tracker Account'
        message = render_to_string('users/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        # IMPORTANT: For local development, send_mail will try to use your email settings.
        # If you don't have them set up, it will print to console.
        # In production, you MUST configure email settings in settings.py (EMAIL_BACKEND, etc.)
        print(f"DEBUG: Preparing to send verification email to {user.email}")
        print(f"DEBUG: Subject: {subject}")
        print(f"DEBUG: Message length: {len(message)}")
        print(f"DEBUG: From email: 'no-reply@mytaller.info'") # Confirm this matches your verified Mailjet sender
        print(f"DEBUG: Domain in link (for reset): {current_site.domain}") # Should be 127.0.0.1:8000

        send_mail(subject, message, 'no-reply@mytaller.info', [user.email])

        print(f"DEBUG: send_mail function called for {user.email}. Check Mailjet logs.")

        messages.success(
            self.request, 'Your account has been created! Please check your email to verify your account.')
        # Important: call super().form_valid(form) AFTER sending email
        return super().form_valid(form)


# --- User Login View ---
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Check if user is verified after login attempt
        if self.request.user.is_authenticated and not self.request.user.is_verified:
            messages.warning(
                self.request, 'Your email is not verified. Please check your inbox for the verification link.')
            logout(self.request)  # Log out if not verified
            return reverse_lazy('login')  # Redirect back to login

        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)

# --- User Logout View ---


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'You have been successfully logged out.')
        return response

    # --- Account Activation View ---


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            login(request, user)  # Log the user in after verification
            messages.success(
                request, 'Thank you for your email verification. Your account is now active.')
            return redirect('home')
        else:
            messages.error(
                request, 'Activation link is invalid or has expired!')
            return redirect('signup')  # Or a dedicated error page
