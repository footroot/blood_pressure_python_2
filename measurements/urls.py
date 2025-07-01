# D:\blood_pressure\blood_pressure_python_2\measurements\urls.py

from django.urls import path
from . import views # Import our views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('add/', views.MeasurementCreateView.as_view(), name='add_measurement'),
    # NEW: URL for editing a measurement
    # <int:pk> captures the primary key of the measurement to be edited
    path('edit/<int:pk>/', views.MeasurementUpdateView.as_view(), name='edit_measurement'),
    # URL for the chart data API endpoint (already there)
    path('data/', views.blood_pressure_data, name='blood_pressure_data'),
]