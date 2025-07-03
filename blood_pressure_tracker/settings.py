# D:\blood_pressure\blood_pressure_python_2\blood_pressure_tracker\settings.py

from decouple import config
from pathlib import Path
from django.urls import reverse_lazy # Import reverse_lazy for URL redirection settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xm)q6rjjhy%9-wtl34g0fb60y1sin2g-o)*07r3e3ju2j8f2#%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig', # Use this instead of just 'users'
    'measurements.apps.MeasurementsConfig', # Use this instead of just 'measurements'
    'django.contrib.sites', # Already included, essential for activation links
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blood_pressure_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # It's generally better to have a project-level 'templates' directory.
        # If your 'base.html' is currently in 'users/templates/', it will still be found
        # because APP_DIRS is True. For project-wide templates, consider:
        'DIRS': [BASE_DIR / 'templates'], # For project-wide templates (e.g., a shared base.html if not in an app)
        'APP_DIRS': True, # This tells Django to look for templates in each app's 'templates' directory
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', # Add this for media files (e.g., user profile pictures)
            ],
        },
    },
]

WSGI_APPLICATION = 'blood_pressure_tracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles' # Uncomment for deployment (run collectstatic)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# Authentication URLs - use reverse_lazy to correctly resolve namespaced URLs
# These are used by Django's built-in views and decorators (e.g., @login_required)
LOGIN_URL = reverse_lazy('users:login')
LOGIN_REDIRECT_URL = reverse_lazy('users:dashboard') # Redirect to dashboard after successful login
LOGOUT_REDIRECT_URL = reverse_lazy('users:login') # Redirect to login after logout

# Django Messages Framework storage (explicitly set for clarity)
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Site Framework (already present, correct for email activation links)
SITE_ID = 1

# Email Configuration
# IMPORTANT: For development/testing, use console backend to see emails in your terminal.
# Comment out the SMTP settings below while in DEBUG=True mode for easy testing.
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production, uncomment and configure your SMTP settings (using decouple for security)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'footroot@mytaller.info' # The email address your users will see the email coming from
SERVER_EMAIL = 'mytaller.info' # For error messages sent by Django (e.g., if DEBUG=False)


# Media files (for uploaded files like profile pictures)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # This will create a 'media' folder in your project root









# from decouple import config
# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-xm)q6rjjhy%9-wtl34g0fb60y1sin2g-o)*07r3e3ju2j8f2#%'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []


# # Application definition

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'users.apps.UsersConfig', # Use this instead of just 'users' 
#     'measurements.apps.MeasurementsConfig', # Use this instead of just 'measurements' 
#     'django.contrib.sites',
#     'widget_tweaks',
#     ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'blood_pressure_tracker.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'users' / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'blood_pressure_tracker.wsgi.application'


# # Database
# # https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# # Password validation
# # https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # Internationalization
# # https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'

# # Default primary key field type
# # https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH_USER_MODEL = 'users.CustomUser'
# LOGIN_URL = '/login/' 
# LOGIN_REDIRECT_URL = '/' # Optional: where to redirect after successful login if 'next' isn't provided
# LOGOUT_REDIRECT_URL = '/login/' # Optional: where to redirect after logout


# SITE_ID = 1

# # Email Configuration for Production 
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST') # Get from environment variable
# EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int) # Get from env, default 587, cast to int 
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool) # Get from env, default True, cast to bool 
# EMAIL_HOST_USER = config('EMAIL_HOST_USER') # Get from environment variable 
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD') # Get from environment variable 
# DEFAULT_FROM_EMAIL = 'footroot@mytaller.info' # The email address your users will see the email coming from 
# SERVER_EMAIL = 'mytaller.info' # For error messages sent by Django (e.g., if DEBUG=False)

# # Custom User Model
# AUTH_USER_MODEL = 'users.CustomUser' # This tells Django to use your custom user model

# # Media files (for profile pictures)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media' # This will create a 'media' folder in your project root
 