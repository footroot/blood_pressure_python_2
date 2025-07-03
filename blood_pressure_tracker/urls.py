# D:\blood_pressure\blood_pressure_python_2\blood_pressure_tracker\urls.py

from django.contrib import admin
from django.urls import path, include
# You imported auth_views, but we won't use them here for password reset
# directly, as they are now handled by users/urls.py with your custom views.
from django.contrib.auth import views as auth_views # This line can be removed or kept, it's not hurting if not used

urlpatterns = [
    path('admin/', admin.site.urls),
    # IMPORTANT: Include the users app URLs with the 'users' namespace
    path('', include('users.urls', namespace='users')), # This line correctly pulls in all URLs from users/urls.py, including password reset
    path('measurements/', include('measurements.urls')), # Our new measurements app URLs

    # --- REMOVE THESE PASSWORD RESET URLs ---
    # These are now handled by your custom views and are included via 'users.urls'
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
]