# measurements/urls.py

from django.urls import path
from . import views # Import our views

urlpatterns = [
    path('dashboard/', views.MeasurementListView.as_view(), name='dashboard'),
    path('add/', views.MeasurementCreateView.as_view(), name='add_measurement'),
]