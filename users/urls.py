# users/urls.py

from django.urls import path
from . import views # Import our views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    # New URL for account activation 
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate_account'), 
]