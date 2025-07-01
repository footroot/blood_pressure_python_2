# D:\blood_pressure\blood_pressure_python_2\measurements\forms.py
from django import forms
from .models import Measurement # Ensure Measurement model is imported

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        # IMPORTANT: 'timestamp' replaces 'date' and 'time'
        # Make sure your Measurement model in models.py has 'timestamp'
        # and DOES NOT have 'date' and 'time' fields anymore.
        fields = ['systolic', 'diastolic', 'pulse', 'weight', 'height', 'timestamp'] # Added 'height'

        widgets = {
            'systolic': forms.NumberInput(attrs={'placeholder': 'Systolic (e.g., 120)'}),
            'diastolic': forms.NumberInput(attrs={'placeholder': 'Diastolic (e.g., 80)'}),
            'pulse': forms.NumberInput(attrs={'placeholder': 'Pulse (e.g., 70)'}),
            # Corrected widget definition for 'weight'
            'weight': forms.NumberInput(attrs={'placeholder': 'Weight (e.g., 70.5)'}),
            # Corrected widget definition for 'height'
            'height': forms.NumberInput(attrs={'placeholder': 'Height (e.g., 1.75 for meters)'}),
            # Corrected widget definition for 'timestamp'
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        labels = {
            'systolic': 'Systolic Blood Pressure (mmHg)',
            'diastolic': 'Diastolic Blood Pressure (mmHg)',
            'pulse': 'Pulse (BPM)',
            'weight': 'Weight (e.g., kg or lbs)',
            'height': 'Height (e.g., meters or cm)', # Label for the new 'height' field
            'timestamp': 'Date & Time of Measurement',
        }

    # Custom validation for the weight field (optional, but good practice)
    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and weight <= 0:
            raise forms.ValidationError("Weight must be a positive value.")
        return weight

    # Custom validation for the height field
    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height is not None and height <= 0:
            raise forms.ValidationError("Height must be a positive value.")
        return height