from django.contrib import admin
from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    """
    How Appointments are viewed on the admin site
    """

    list_display = ('location', 'date', 'time', 'endTime', 'patient_ID', 'doctor_ID',)
    list_filter = ('location', 'date', 'patient_ID', 'doctor_ID',)

admin.site.register(Appointment, AppointmentAdmin)
