# D:\blood_pressure\blood_pressure_python_2\blood_pressure_tracker\urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

# A simple view function to handle the root URL based on authentication status
def root_redirect_view(request):
    if request.user.is_authenticated:
        # If logged in, redirect to the dashboard using the 'users' namespace
        return redirect('users:dashboard')
    else:
        # If not logged in, redirect to the login page using the 'users' namespace
        return redirect('users:login')

urlpatterns = [
    path('admin/', admin.site.urls),

    # This line handles the root URL (e.g., http://127.0.0.1:8000/)
    # It redirects to either the dashboard or the login page based on user's login status.
    path('', root_redirect_view, name='home'),

    # Include all URLs from the 'users' app under the 'accounts/' prefix
    # and assign them to the 'users' namespace.
    # This means URLs will now be like /accounts/signup/, /accounts/dashboard/, etc.
    path('accounts/', include('users.urls', namespace='users')),

    # Include URLs from the measurements app
    path('measurements/', include('measurements.urls', namespace='measurements')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)