# D:\blood_pressure\blood_pressure_python_2\users\views.py

from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib.auth.tokens import default_token_generator

# Import CustomUser and forms
from .models import CustomUser, Medication
from .forms import CustomUserCreationForm, UserProfileUpdateForm, MedicationForm

# Ensure Measurement model is imported for dashboard/calendar context
from measurements.models import Measurement # Assuming measurements app is correctly configured

# --- Signup View ---
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # --- Email Sending Logic ---
            current_site = get_current_site(request)
            mail_subject = 'Activate your BP Tracker account.'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            try:
                email.send()
                messages.info(request, ('Please confirm your email address to complete the registration. Check your spam folder if you don\'t see it.'))
                return redirect('users:account_activation_sent')
            except Exception as e:
                print(f"Error sending activation email: {e}")
                messages.error(request, 'Failed to send activation email. Please try again later.')
                return render(request, 'users/signup.html', {'form': form})
        else:
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
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Your account is now active and you are logged in.')
        return redirect('users:dashboard')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('users:signup')

# --- Page to inform user to check email ---
def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')


@login_required
def dashboard(request):
    if not request.user.is_active:
        messages.warning(request, 'Please activate your account by confirming your email address.')
        return redirect('users:account_activation_sent')

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
    month_measurements = Measurement.objects.filter(
        user=request.user,
        timestamp__year=current_year,
        timestamp__month=current_month
    ).order_by('timestamp')

    # Group measurements by day for easy lookup in template
    measurements_by_day = defaultdict(list)
    for measurement in month_measurements:
        measurements_by_day[measurement.timestamp.day].append(measurement)

    # Fetch active medications for dashboard display (limited to a few for brevity)
    dashboard_medications = Medication.objects.filter(
        user=request.user
    ).order_by('-is_active', 'name')[:5]

    context = {
        'user': request.user,
        'recent_measurements': recent_measurements,
        'today': today,
        'month_calendar': month_calendar,
        'day_names': day_names,
        'measurements_by_day': measurements_by_day,
        'month': current_month,
        'year': current_year,
        'dashboard_medications': dashboard_medications,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:profile_edit')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'users/profile_edit.html', context)

@login_required
def medication_manage(request):
    if not request.user.is_active:
        messages.warning(request, 'Please activate your account by confirming your email address.')
        return redirect('users:account_activation_sent')

    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save(commit=False)
            medication.user = request.user
            medication.save()
            messages.success(request, 'Medication added successfully!')
            return redirect('users:medication_manage')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MedicationForm()

    medications = Medication.objects.filter(user=request.user).order_by('-is_active', 'name')

    context = {
        'form': form,
        'medications': medications,
        'user': request.user,
    }
    return render(request, 'users/medication_manage.html', context)

@login_required
def medication_delete(request, pk):
    """
    Deletes a specific medication for the logged-in user.
    Requires a POST request for security.
    """
    medication = get_object_or_404(Medication, pk=pk, user=request.user)

    if request.method == 'POST':
        medication.delete()
        messages.success(request, f'Medication "{medication.name}" deleted successfully.')
        return redirect('users:medication_manage')
    else:
        messages.warning(request, f'Confirmation required to delete "{medication.name}".')
        return redirect('users:medication_manage')

@login_required
def medication_edit(request, pk):
    """
    Handles editing an existing medication for the logged-in user.
    """
    medication = get_object_or_404(Medication, pk=pk, user=request.user)

    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            messages.success(request, f'Medication "{medication.name}" updated successfully.')
            return redirect('users:medication_manage')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MedicationForm(instance=medication)

    context = {
        'form': form,
        'medication': medication,
        'user': request.user,
    }
    return render(request, 'users/medication_edit.html', context)