# D:\blood_pressure\blood_pressure_python_2\users\models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import os # Import os module for profile picture path

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_pics/user_<id>/<filename>
    # Ensures unique path for each user's profile picture
    return os.path.join(f'profile_pics/user_{instance.id}', filename)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False) # Ensures new users are inactive by default

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True) # Superusers are verified by default

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # --- NEW PROFILE FIELDS START HERE ---
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    address = models.TextField(
        _("address"),
        blank=True,
        null=True,
        help_text=_("Full street address")
    )
    phone_mobile = models.CharField(
        _("mobile phone"),
        max_length=20,
        blank=True,
        null=True
    )
    phone_landline = models.CharField(
        _("landline phone"),
        max_length=20,
        blank=True,
        null=True
    )
    phone_emergency = models.CharField(
        _("emergency contact phone"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Another phone number in case of emergency")
    )
    profile_picture = models.ImageField(
        _("profile picture"),
        upload_to=user_directory_path,
        blank=True,
        null=True,
        default='profile_pics/default_profile.png' # You'll need to create this default image
    )
    # --- NEW PROFILE FIELDS END HERE ---

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email is already unique, no other fields required at signup

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        # Prefer full name, fallback to email
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    # --- Overriding AbstractBaseUser methods ---
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email # Fallback if no name provided

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        if self.first_name:
            return self.first_name
        return self.email # Fallback

    # --- Additional method for display in templates ---
    @property
    def get_full_name_display(self):
        """
        Returns the full name for display on the dashboard, falling back to email if empty.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

# --- NEW MEDICATION MODEL START HERE ---
class Medication(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='medications',
        verbose_name=_("user")
    )
    name = models.CharField(_("medication name"), max_length=255)
    dosage = models.CharField(_("dosage"), max_length=100, blank=True, null=True,
                              help_text=_("e.g., 10mg, 2 tablets, 5ml"))
    frequency = models.CharField(_("frequency"), max_length=255, blank=True, null=True,
                                 help_text=_("e.g., Once daily, Twice a day, Every other day"))
    notes = models.TextField(_("notes"), blank=True, null=True,
                             help_text=_("Any additional notes about the medication"))
    start_date = models.DateField(_("start date"), default=timezone.now)
    end_date = models.DateField(_("end date"), blank=True, null=True,
                                help_text=_("Date medication was stopped, if applicable"))
    is_active = models.BooleanField(_("is currently active"), default=True,
                                    help_text=_("Is the user currently taking this medication?"))

    class Meta:
        verbose_name = _("medication")
        verbose_name_plural = _("medications")
        ordering = ['-is_active', 'name'] # Active medications first, then by name
        unique_together = ('user', 'name', 'dosage', 'frequency') # Prevent exact duplicates for a user

    def __str__(self):
        return f"{self.name} ({self.dosage or 'No Dosage'}) - {self.user.email}"

# --- NEW MEDICATION MODEL END HERE ---