# D:\blood_pressure\blood_pressure_python_2\measurements\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
# NEW IMPORT: Add UpdateView for editing functionality
from django.views.generic import UpdateView
# NEW IMPORT: Add UserPassesTestMixin for security (to ensure users only edit their own data)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

# Imports for the models and forms
from .models import Measurement
from .forms import MeasurementForm

# NEW IMPORTS for the API endpoint (already there)
from django.http import JsonResponse
import json  # Although not directly used for JsonResponse, good to have if you need custom JSON serialization
from datetime import datetime


class DashboardView(LoginRequiredMixin, ListView):
    model = Measurement
    template_name = 'measurements/dashboard.html'
    context_object_name = 'measurements'
    paginate_by = 10  # If you want pagination

    def get_queryset(self):
        # Ensure only the logged-in user's measurements are displayed, ordered by timestamp
        # Order descending for list view
        return Measurement.objects.filter(user=self.request.user).order_by('-timestamp')


class MeasurementCreateView(LoginRequiredMixin, CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'measurements/add_measurement.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Measurement added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


# NEW: View for editing an existing measurement
# Added UserPassesTestMixin
class MeasurementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'measurements/edit_measurement.html'  # We will create this template
    # Redirect to dashboard after successful edit
    success_url = reverse_lazy('dashboard')
    # Name for the object in the template context
    context_object_name = 'measurement'

    # Ensure only the owner can edit their own measurement
    def test_func(self):
        measurement = self.get_object()
        return measurement.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Measurement updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


# NEW: API endpoint for chart data (already there)
# This view provides historical blood pressure and pulse data in JSON format for charting.
def blood_pressure_data(request):
    # Ensure only authenticated users can access their data
    if not request.user.is_authenticated:
        # Return a 401 Unauthorized response if the user is not logged in
        return JsonResponse({'error': 'Authentication required'}, status=401)

    # Fetch measurements for the current user, ordered chronologically for the chart
    measurements = Measurement.objects.filter(
        user=request.user).order_by('timestamp')

    # Prepare the data structure required by Chart.js
    data = {
        'labels': [],    # To store formatted timestamps for the X-axis
        'systolic': [],  # To store systolic blood pressure readings
        'diastolic': [],  # To store diastolic blood pressure readings
        'pulse': [],     # To store pulse readings
    }

    # Iterate through the measurements and populate the data dictionary
    for m in measurements:
        # Format timestamp for better chart readability (e.g., '2025-07-01 14:30')
        data['labels'].append(m.timestamp.strftime('%Y-%m-%d %H:%M'))
        # Convert numeric values to float to ensure compatibility with charting libraries
        data['systolic'].append(float(m.systolic))
        data['diastolic'].append(float(m.diastolic))
        data['pulse'].append(float(m.pulse))

    # Return the data as a JSON response
    return JsonResponse(data)
