# D:\blood_pressure\blood_pressure_python_2\users\urls.py

from django.urls import path, include # Add 'include' for the possibility of using it later, though not strictly needed here
from django.contrib.auth import views as auth_views
from . import views as users_views # Import our views
from measurements import views as measurements_views

app_name = 'users' # <--- This registers the namespace

urlpatterns = [
    path('', users_views.HomePageView.as_view(), name='home'),
    path('signup/', users_views.SignUpView.as_view(), name='signup'),
    path('login/', users_views.CustomLoginView.as_view(), name='login'),
    path('logout/', users_views.CustomLogoutView.as_view(), name='logout'),
    # New URL for account activation
    path('activate/<uidb64>/<token>/', users_views.ActivateAccountView.as_view(), name='activate_account'),

    # Dashboard URL (already present)
    path('dashboard/', measurements_views.dashboard_view, name='dashboard'),

    # --- Password Reset URLs (ADDED THESE LINES) ---
    path('password_reset/',
         users_views.CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         users_views.CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         users_views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         users_views.CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]