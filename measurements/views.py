# measurements/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View # Import View for base class
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin # For authentication and permission handling
from django.contrib import messages

from .models import Measurement
from .forms import MeasurementForm

# --- Custom Mixin for Email Verification ---
class EmailVerifiedRequiredMixin(AccessMixin):
    """
    Verify that the current user is authenticated and their email is verified.
    Redirects to login if not authenticated, or shows error if not verified.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission() # Redirects to LOGIN_URL

        if not request.user.is_verified:
            messages.error(request, 'Please verify your email address to access this page.')
            return redirect('home') # Or a dedicated unverified page

        return super().dispatch(request, *args, **kwargs)

# --- Dashboard View (List all measurements for the logged-in user) ---
class MeasurementListView(LoginRequiredMixin, EmailVerifiedRequiredMixin, ListView):
    model = Measurement
    template_name = 'measurements/dashboard.html'
    context_object_name = 'measurements' # Name of the variable in the template
    paginate_by = 10 # Optional: Add pagination for many measurements

    def get_queryset(self):
        # Only show measurements for the currently logged-in user
        return Measurement.objects.filter(user=self.request.user)

# --- Add New Measurement View ---
class MeasurementCreateView(LoginRequiredMixin, EmailVerifiedRequiredMixin, CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'measurements/add_measurement.html'
    success_url = reverse_lazy('dashboard') # Redirect to dashboard after adding

    def form_valid(self, form):
        # Assign the current user to the measurement before saving
        form.instance.user = self.request.user
        messages.success(self.request, 'Blood pressure measurement saved successfully!')
        return super().form_valid(form)