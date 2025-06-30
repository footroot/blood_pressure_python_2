# D:\blood_pressure\blood_pressure_python_2\measurements\models.py

from django.db import models
from django.conf import settings # To get the AUTH_USER_MODEL
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
# from django.conf import settings # This import is redundant, already imported above

class Measurement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='measurements'
    )
    systolic = models.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(250)],
        help_text="Top number (systolic)"
    )
    diastolic = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(150)],
        help_text="Bottom number (diastolic)"
    )
    pulse = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        help_text="Heart rate (beats per minute)"
    )
    # Add the new weight field here
    weight = models.DecimalField(
        max_digits=5,      # e.g., allows numbers up to 999.99 (3 digits before, 2 after)
        decimal_places=2,  # Stores two decimal places
        null=True,         # Allows the field to be NULL in the database
        blank=True,        # Allows the field to be left empty in forms
        help_text="Weight (e.g., kg or lbs. Please use consistent units, e.g., 75.50)"
    )
    # Using auto_now_add=True for creation time
    # This will automatically set the field to now when the object is first created.
    timestamp = models.DateTimeField(default=timezone.now) # Changed to default for manual entry flexibility

    class Meta:
        ordering = ['-timestamp'] # Order by newest measurements first
        verbose_name = "Blood Pressure Measurement"
        verbose_name_plural = "Blood Pressure Measurements"

    def __str__(self):
        return f"{self.user.email} - {self.systolic}/{self.diastolic} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

    @property
    def bp_category(self):
        # This is a simple categorization. Real medical advice should be sought.
        if self.systolic < 120 and self.diastolic < 80:
            return "Normal"
        elif (120 <= self.systolic < 130) and self.diastolic < 80:
            return "Elevated"
        elif (130 <= self.systolic < 140) or (80 <= self.diastolic < 90):
            return "High Blood Pressure (Hypertension Stage 1)"
        elif (140 <= self.systolic) or (90 <= self.diastolic):
            return "High Blood Pressure (Hypertension Stage 2)"
        elif (self.systolic > 180 and self.diastolic > 120): # Note: This condition might overlap. Consider ordering.
            return "Hypertensive Crisis"
        else:
            return "Uncategorized"