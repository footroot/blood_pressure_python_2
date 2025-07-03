# D:\blood_pressure\blood_pressure_python_2\users\views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from calendar import Calendar
from collections import defaultdict
from django.http import JsonResponse
import datetime

# For email verification
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator # This is the standard token generator

# Import CustomUser and forms
from .models import CustomUser
from .forms import CustomUserCreationForm, UserProfileUpdateForm

# Ensure Measurement model is imported for dashboard/calendar context
from measurements.models import Measurement # Assuming measurements app is correctly configured

# --- Signup View ---
def signup(request):
    if request.method == 'POST':
        # Ensure request.FILES is passed if profile picture is part of CustomUserCreationForm
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # --- START CHANGE ---
            # Remove commit=False and the subsequent lines.
            # The manager's create_user method (in models.py) will now set is_active=False.
            user = form.save()
            # --- END CHANGE ---

            # --- Email Sending Logic ---
            current_site = get_current_site(request)
            mail_subject = 'Activate your BP Tracker account.'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user.email # Use user.email for the recipient
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            try:
                email.send()
                messages.info(request, ('Please confirm your email address to complete the registration. Check your spam folder if you don\'t see it.'))
                return redirect('users:account_activation_sent') # Redirect to info page
            except Exception as e:
                print(f"Error sending activation email: {e}") # Print error to console
                messages.error(request, 'Failed to send activation email. Please try again later.')
                # Optional: If email sending is critical, you might want to delete the user or mark for review
                # user.delete()
                return render(request, 'users/signup.html', {'form': form}) # Re-render signup with error

        else:
            # Form is not valid, re-render with errors
            for field in form:
                if field.errors:
                    for error in field.errors:
                        messages.error(request, f"{field.label}: {error}")
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# --- Account Activation View ---
# This view handles the link clicked by the user in the email
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        # --- START CHANGE ---
        user.is_verified = True # UNCOMMENT THIS LINE
        # --- END CHANGE ---
        user.save()
        login(request, user) # Automatically log in the user after activation
        messages.success(request, 'Thank you for your email confirmation. Your account is now active and you are logged in.')
        return redirect('users:dashboard') # Redirect to dashboard after successful activation
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('users:signup') # Redirect to signup with an error message

# --- Page to inform user to check email ---
def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')


@login_required
def dashboard(request):
    # Ensure only active users can access dashboard
    if not request.user.is_active:
        messages.warning(request, 'Please activate your account by confirming your email address.')
        # You might want to log them out or redirect to a more specific "account not active" page
        return redirect('users:account_activation_sent') # Send them back to the check email page

    # Fetch recent measurements for the logged-in user
    recent_measurements = Measurement.objects.filter(user=request.user).order_by('-timestamp')[:10]

    # Calendar data (for current month)
    today = timezone.localdate()
    current_year = today.year
    current_month = today.month

    cal = Calendar()
    month_calendar = cal.monthdays2calendar(current_year, current_month)

    # Prepare day names for calendar header
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # Fetch all measurements for the current month for the logged-in user
    # Filter by year and month
    month_measurements = Measurement.objects.filter(
        user=request.user,
        timestamp__year=current_year,
        timestamp__month=current_month
    ).order_by('timestamp')

    # Group measurements by day for easy lookup in template
    measurements_by_day = defaultdict(list)
    for measurement in month_measurements:
        measurements_by_day[measurement.timestamp.day].append(measurement)

    context = {
        'user': request.user, # Pass the custom user object
        'recent_measurements': recent_measurements,
        'today': today,
        'month_calendar': month_calendar,
        'day_names': day_names,
        'measurements_by_day': measurements_by_day,
        'month': current_month,
        'year': current_year,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        # Pass instance=request.user to edit the existing user object
        # Pass request.FILES to handle profile picture upload
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!') # Add a success message
            return redirect('users:profile_edit') # Redirect back to profile edit or dashboard
        else:
            messages.error(request, 'Please correct the error below.') # Add an error message
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user # Pass user for display in template
    }
    return render(request, 'users/profile_edit.html', context)