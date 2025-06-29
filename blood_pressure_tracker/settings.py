from decouple import config
from pathlib import Path

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
    'django.contrib.sites',
    'users.apps.UsersConfig',
    'measurements.apps.MeasurementsConfig', # Our new measurements app
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
        'DIRS': [BASE_DIR / 'users' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
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

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = '/login/' 
LOGIN_REDIRECT_URL = '/' # Optional: where to redirect after successful login if 'next' isn't provided
LOGOUT_REDIRECT_URL = '/login/' # Optional: where to redirect after logout


SITE_ID = 1

# Email settings for development 
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Prints emails to console 
# OR for saving to a file (more useful if you want to inspect HTML emails): 
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend' 
# EMAIL_FILE_PATH = BASE_DIR / 'sent_emails' # Make sure this directory exists!

# Email Configuration for Production 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST') # Get from environment variable
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int) # Get from env, default 587, cast to int 
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool) # Get from env, default True, cast to bool 
EMAIL_HOST_USER = config('EMAIL_HOST_USER') # Get from environment variable 
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD') # Get from environment variable 
DEFAULT_FROM_EMAIL = 'footroot@mytaller.info' # The email address your users will see the email coming from 
SERVER_EMAIL = 'errors@mytaller.info' # For error messages sent by Django (e.g., if DEBUG=False) 