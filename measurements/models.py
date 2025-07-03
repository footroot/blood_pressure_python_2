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
    height = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Height (e.g., in meters: 1.75 or in cm: 175.00 - if in cm, remember to divide by 100 for BMI)"
    )
    # Changed from auto_now_add=True to default=timezone.now to allow manual editing of timestamp if needed
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Blood Pressure Measurement"
        verbose_name_plural = "Blood Pressure Measurements"

    def __str__(self):
        return f"{self.user.email} - {self.systolic}/{self.diastolic} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

    @property
    def bp_category(self):
        """
        Categorizes blood pressure based on AHA/ACC 2017 guidelines,
        with an added 'Low' category as requested.
        """
        s = self.systolic
        d = self.diastolic

        # Low Blood Pressure (Hypotension) - ADDED THIS CONDITION FIRST
        if s < 90 or d < 60:
            return "Low"
        # Normal Blood Pressure
        elif s < 120 and d < 80:
            return "Normal"
        # Elevated
        elif (120 <= s < 130) and d < 80:
            return "Elevated"
        # High Blood Pressure (Hypertension Stage 1)
        elif (130 <= s < 140) or (80 <= d < 90):
            return "High Blood Pressure (Hypertension Stage 1)"
        # High Blood Pressure (Hypertension Stage 2)
        elif (s >= 140) or (d >= 90):
            return "High Blood Pressure (Hypertension Stage 2)"
        # Hypertensive Crisis (emergency care needed) - Stricter condition (AND)
        # You might consider 'or' here if either being critical is enough for crisis.
        elif (s > 180 and d > 120):
            return "Hypertensive Crisis"
        else:
            return "Uncategorized" # Should ideally not be reached with typical values

    @property
    def bmi(self):
        """
        Calculates Body Mass Index (BMI).
        Assumes weight is in kilograms and height is in meters.
        BMI = weight (kg) / (height (m))^2
        """
        if self.weight is not None and self.height is not None:
            try:
                # Convert Decimal to float for calculation precision
                height_m = float(self.height)
                weight_kg = float(self.weight)

                if height_m > 0:
                    # If height is stored in centimeters (e.g., 175.00), convert to meters: (height_m / 100)
                    # Based on your help_text "in meters: 1.75 or in cm: 175.00 - if in cm, remember to divide by 100 for BMI)"
                    # I'm assuming 'self.height' is already in meters if you input 1.75.
                    # If you consistently input in CM, you must add /100 here.
                    # For now, I'll keep it as if it's already meters to align with the direct BMI formula.
                    # If you input 175 for 1.75 meters, change height_m to (height_m / 100).
                    return round(weight_kg / (height_m ** 2), 2)
                else:
                    return None # Height cannot be zero or non-positive
            except (ValueError, TypeError):
                return None # Handle cases where conversion fails
        return None # Return None if weight or height is not available

    @property
    def bmi_category(self):
        """
        Categorizes BMI into standard classifications (e.g., CDC/WHO guidelines).
        Requires the 'bmi' property to be calculated first.
        """
        if self.bmi is None:
            return "N/A" # Or "No BMI data"
        
        bmi_val = self.bmi

        if bmi_val < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_val <= 24.9:
            return "Normal weight" # Aligns with "fit"
        elif 25.0 <= bmi_val <= 29.9:
            return "Overweight"
        elif 30.0 <= bmi_val <= 34.9:
            return "Obese (Class I)"
        elif 35.0 <= bmi_val <= 39.9:
            return "Obese (Class II)"
        else: # bmi_val >= 40.0
            return "Obese (Class III)"