# measurements/admin.py

from django.contrib import admin
from .models import Measurement

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('user', 'systolic', 'diastolic', 'pulse', 'timestamp', 'bp_category')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__email', 'systolic', 'diastolic')
    date_hierarchy = 'timestamp' # Adds date-based drilldown navigation
    readonly_fields = ('bp_category',) # Make bp_category read-only in admin form