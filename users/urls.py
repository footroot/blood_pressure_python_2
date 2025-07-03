# D:\blood_pressure\blood_pressure_python_2\users\urls.py

from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    # User authentication and profile URLs
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="users:login"), name="logout"
    ),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    # --- EMAIL ACTIVATION URLs ---
    path(
        "account_activation_sent/",
        views.account_activation_sent,
        name="account_activation_sent",
    ),
    # CORRECTED: Relaxed the token regex length to allow up to 40 characters for the second part
    re_path(r"activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$",
            views.activate, name="activate"),
    # -----------------------------
    # Include Django's default authentication URLs for password reset, etc.
    path("", include("django.contrib.auth.urls")),
]