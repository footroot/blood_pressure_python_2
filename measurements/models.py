# D:\blood_pressure\blood_pressure_python_2\measurements\models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

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
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight (e.g., kg or lbs, specify units consistently)"
    )
    # Add the new height field here
    height = models.DecimalField(
        max_digits=4,      # e.g., 99.99 (for meters) or 999.9 (for cm)
        decimal_places=2,  # e.g., allows two decimal places (e.g., 1.75 meters)
        null=True,         # Allows the field to be NULL in the database
        blank=True,        # Allows the field to be blank in forms
        help_text="Height (e.g., in meters: 1.75 or in cm: 175.00)"
    )
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Blood Pressure Measurement"
        verbose_name_plural = "Blood Pressure Measurements"

    def __str__(self):
        return f"{self.user.email} - {self.systolic}/{self.diastolic} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

    @property
    def bp_category(self):
        if self.systolic < 120 and self.diastolic < 80:
            return "Normal"
        elif (120 <= self.systolic < 130) and self.diastolic < 80:
            return "Elevated"
        elif (130 <= self.systolic < 140) or (80 <= self.diastolic < 90):
            return "High Blood Pressure (Hypertension Stage 1)"
        elif (140 <= self.systolic) or (90 <= self.diastolic):
            return "High Blood Pressure (Hypertension Stage 2)"
        elif (self.systolic > 180 and self.diastolic > 120):
            return "Hypertensive Crisis"
        else:
            return "Uncategorized"

    # You can add a property here to calculate BMI later if height and weight are present
    @property
    def bmi(self):
        if self.weight and self.height:
            # Assuming weight in kg and height in meters for standard BMI calculation
            # BMI = weight (kg) / (height (m))^2
            # You might need to convert units if you're storing in lbs/cm
            try:
                # Ensure height is not zero to avoid division by zero
                if float(self.height) > 0:
                    # Convert Decimal to float for calculation precision
                    return round(float(self.weight) / (float(self.height) ** 2), 2)
                else:
                    return None # Height cannot be zero
            except (ValueError, TypeError):
                return None # Handle cases where conversion fails
        return None # Return None if weight or height is not available