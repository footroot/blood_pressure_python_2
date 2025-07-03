# D:\blood_pressure\blood_pressure_python_2\measurements\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages # Already here, but confirming
from datetime import date, timedelta, datetime # Ensure datetime is imported for robust timestamp parsing
import calendar
from django.db.models import F

# Import your Measurement model and MeasurementForm
from .models import Measurement
from .forms import MeasurementForm # <--- MAKE SURE THIS IS IMPORTED!

# Helper function to get common calendar context
def get_calendar_context(request, current_base_url_name, year=None, month=None):
    today = date.today()

    if year and month:
        try:
            selected_date = date(int(year), int(month), 1) # Convert year/month to int
        except ValueError:
            # Handle invalid year/month, fallback to current month
            selected_date = date(today.year, today.month, 1)
    else:
        selected_date = date(today.year, today.month, 1) # Default to current month if no year/month provided

    year = selected_date.year
    month = selected_date.month
    month_name = calendar.month_name[month]

    # Calculate previous and next month dates
    first_day_current_month = date(year, month, 1)
    last_day_prev_month = first_day_current_month - timedelta(days=1)
    first_day_next_month = first_day_current_month + timedelta(days=calendar.monthrange(year, month)[1])

    # Generate query parameters for prev/next month URLs
    prev_month_params = f"year={last_day_prev_month.year}&month={last_day_prev_month.month}"
    next_month_params = f"year={first_day_next_month.year}&month={first_day_next_month.month}"

    # Generate a calendar object starting Monday (0=Mon, 6=Sun)
    cal = calendar.Calendar(0)
    month_calendar = cal.monthdays2calendar(year, month)

    # Fetch measurements for the current month for the logged-in user
    measurements = Measurement.objects.filter(
        user=request.user,
        timestamp__year=year,
        timestamp__month=month
    ).order_by('timestamp')

    # Organize measurements by day
    measurements_by_day = {}
    for measurement in measurements:
        day = measurement.timestamp.day
        if day not in measurements_by_day:
            measurements_by_day[day] = []
        measurements_by_day[day].append(measurement)

    # Day names for the calendar header (e.g., ['Mon', 'Tue', ...])
    day_names = [calendar.day_abbr[i] for i in cal.iterweekdays()]

    context = {
        'month_calendar': month_calendar,
        'measurements_by_day': measurements_by_day,
        'day_names': day_names,
        'today': today,
        'month': month,
        'year': year,
        'month_name': month_name,
        'prev_month_params': prev_month_params,
        'next_month_params': next_month_params,
        'base_url': reverse(current_base_url_name),
    }
    return context


# --- Dashboard View (MOVED FROM users/views.py) ---
@login_required
def dashboard_view(request, year=None, month=None):
    today = date.today()
    # Convert year/month from URL/GET params to int, or use today's date
    if year is None:
        year = today.year
    else:
        year = int(year)
    if month is None:
        month = today.month
    else:
        month = int(month)

    # Get calendar context. Pass request.GET's year/month if present.
    # This allows navigation of the calendar directly on the dashboard.
    # 'users:dashboard' is the URL name for the dashboard view.
    calendar_context = get_calendar_context(request, 'users:dashboard',
                                            year=request.GET.get('year', year), # Use GET params for calendar navigation
                                            month=request.GET.get('month', month))

    # Prepare dashboard specific data
    recent_measurements = Measurement.objects.filter(user=request.user).order_by('-timestamp')[:5] # Get last 5

    dashboard_data = {
        'user': request.user,
        'recent_measurements': recent_measurements, # Pass recent measurements to the template
    }

    # Combine dashboard data with calendar context
    context = {**dashboard_data, **calendar_context}

    # Render the dashboard template (which remains in users/templates)
    return render(request, 'users/dashboard.html', context)


# --- Add Measurement View (UPDATED TO USE MeasurementForm) ---
@login_required
def add_measurement(request):
    if request.method == 'POST':
        # Instantiate the form with the POST data
        form = MeasurementForm(request.POST)
        if form.is_valid():
            # Save the form instance to the database, but don't commit yet
            # because we need to set the user
            measurement = form.save(commit=False)
            measurement.user = request.user # Assign the current logged-in user
            measurement.save() # Now save the measurement to the database
            messages.success(request, 'Blood pressure measurement added successfully!')
            return redirect('users:dashboard') # Redirect on success
        else:
            # If the form is NOT valid, messages.error will be handled by the template if setup.
            # The 'form' object will now contain the errors, which the template will display.
            messages.error(request, 'Please correct the errors below.')
    else: # This block handles GET requests (when the page is first loaded)
        # For a GET request, create an empty form instance
        form = MeasurementForm() # <--- This ensures the form fields are displayed

    # Render the template, always passing the 'form' instance to the context
    return render(request, 'measurements/add_measurement.html', {'form': form})


# --- Measurement List View ---
@login_required
def measurement_list(request):
    measurements = Measurement.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'measurements/measurement_list.html', {'measurements': measurements})


# --- Edit Measurement View (UPDATED TO USE MeasurementForm) ---
@login_required
def edit_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk, user=request.user)

    if request.method == 'POST':
        # Instantiate the form with POST data and the existing measurement instance
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save() # Save the updated measurement
            messages.success(request, 'Measurement updated successfully!')
            return redirect('users:dashboard') # Redirect on success
        else:
            # If the form is NOT valid, display errors
            messages.error(request, 'Please correct the errors below.')
    else: # GET request
        # Instantiate the form with the existing measurement data to pre-populate it
        form = MeasurementForm(instance=measurement)

    # Render the template, passing the form instance and the measurement object
    return render(request, 'measurements/edit_measurement.html', {'form': form, 'measurement': measurement})


# --- Delete Measurement View ---
@login_required
def delete_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk, user=request.user)
    if request.method == 'POST':
        measurement.delete()
        messages.success(request, 'Measurement deleted successfully!')
        return redirect('users:dashboard')
    # For GET request, just render the confirmation page
    return render(request, 'measurements/delete_measurement_confirm.html', {'measurement': measurement})


# --- Blood Pressure Data for Charting ---
@login_required
def blood_pressure_data(request):
    # This function provides data for charting.
    # It fetches the last 30 days of measurements for the current user.
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    measurements = Measurement.objects.filter(
        user=request.user,
        timestamp__date__range=[start_date, end_date]
    ).order_by('timestamp')

    # Prepare data in a format suitable for charting libraries (e.g., Chart.js)
    data = {
        'labels': [],    # Dates/times for X-axis
        'systolic': [],  # Systolic readings
        'diastolic': [], # Diastolic readings
        'pulse': [],     # Pulse readings
    }

    for m in measurements:
        # Format timestamp as a string for display on the chart's x-axis
        data['labels'].append(m.timestamp.strftime('%Y-%m-%d %H:%M'))
        data['systolic'].append(m.systolic)
        data['diastolic'].append(m.diastolic)
        data['pulse'].append(m.pulse)

    # Return the data as a JSON response
    return JsonResponse(data)


# --- Calendar View (for general calendar, if different from dashboard) ---
@login_required
def calendar_view(request, year=None, month=None):
    # Determine the initial date for the calendar context based on URL kwargs
    selected_date = None
    if year and month:
        try:
            selected_date = date(year, month, 1)
        except ValueError:
            # Fallback if invalid year/month in URL
            pass

    # Call the helper function, passing the name of this view for URL generation
    context = get_calendar_context(request, 'measurements:calendar_view', year=selected_date.year if selected_date else None, month=selected_date.month if selected_date else None)

    return render(request, 'measurements/calendar_view.html', context)