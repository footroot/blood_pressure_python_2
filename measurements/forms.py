# measurements/forms.py

from django import forms
from .models import Measurement

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['systolic', 'diastolic', 'pulse']
        # Optionally add 'timestamp' if you want users to be able to
        # specify the date/time of the measurement, otherwise it defaults to now.
        # If you add 'timestamp', consider using a DateInput/DateTimeInput widget.

        widgets = {
            'systolic': forms.NumberInput(attrs={'placeholder': 'Systolic (e.g., 120)'}),
            'diastolic': forms.NumberInput(attrs={'placeholder': 'Diastolic (e.g., 80)'}),
            'pulse': forms.NumberInput(attrs={'placeholder': 'Pulse (e.g., 70)'}),
        }
        labels = {
            'systolic': 'Systolic Blood Pressure (mmHg)',
            'diastolic': 'Diastolic Blood Pressure (mmHg)',
            'pulse': 'Pulse (BPM)',
        }