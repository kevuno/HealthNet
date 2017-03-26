from django.db import models
from django.utils import timezone


class Entry(models.Model):
    """
    An entry for the log
    ------------------------------------------------------------------------------------
    user:       The user conducting the activity
    activity:   The action that the user is conducting
    time:       The time at which the activity was conducted
    trigger:    The location in the code where the log entry was created and added
    ------------------------------------------------------------------------------------
    user:       request.user.username
    activity:   'Created Account', 'Updated Patient',
                'Updated Appointment', 'Created Appointment', 'Deleted Appointment',
                'Logged In', 'Logged Out',
                'Sent Message', 'Deleted Message'
                'Transferred patient name to hospital name',
                'Updated patient name's medical information'
                'Exported Information'
                'Created test for patient name'
                'Created prescription for patient name'
    time:       now
    trigger:    'userprofile.views.PatientUserFormView', 'userprofile.views.UpdateProfileView',
                'appointment.views.AppointmentEdit', 'appointment.views.create','appointment.views.appointment_detail',
                'home.views.logLogin', 'home.views.goodbye',
                'messaging.views.ComposeMessage', 'messaging.views.message_detail'
                'userprofile.views.export'
                'employee.views.patient_options'
    """

    class Meta:
        verbose_name_plural = "entries"

    user = models.CharField(default=None, max_length=15, null=True)
    activity = models.CharField(default=None, max_length=100, null=True)
    time = models.DateTimeField(default=timezone.now())
    trigger = models.CharField(default=None, max_length=20, null=True)

    def __str__(self):
        return self.activity
