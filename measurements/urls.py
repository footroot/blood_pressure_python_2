# D:\blood_pressure\blood_pressure_python_2\measurements\urls.py

from django.urls import path
from . import views # Import our views

app_name = 'measurements' # <--- ADD THIS LINE HERE to register the namespace

urlpatterns = [
    # Add Measurement
    path("add/", views.add_measurement, name="add_measurement"),

    # List Measurements
    path('list/', views.measurement_list, name='measurement_list'),

    # Edit Measurement
    path("edit/<int:pk>/", views.edit_measurement, name="edit_measurement"),

    # Delete Measurement
    path("delete/<int:pk>/", views.delete_measurement, name="delete_measurement"),

    # Chart Data API
    path("data/", views.blood_pressure_data, name="blood_pressure_data"),

    # Calendar Views
    # Note: If these names cause issues with the calendar logic,
    # you might want to use just 'calendar_view' and handle logic in view.
    # However, 'calendar_view' is used in get_calendar_context, so 'calendar_view' might be expected.
    # Let's adjust 'calendar_view_current' to 'calendar_view' as per the get_calendar_context usage.
    path("calendar/", views.calendar_view, name="calendar_view"), # Name is now just 'calendar_view'
    path("calendar/<int:year>/<int:month>/", views.calendar_view, name="calendar_view_month"),

    # REMOVED: path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # This URL pattern belongs only in users/urls.py, pointing to the function-based dashboard_view.
]