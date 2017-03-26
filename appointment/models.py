from django.db import models
from userprofile.models import Doctor, Patient, Nurse
from django.utils import timezone
import datetime

class Appointment(models.Model):
    patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1) #null = True?
    doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    location = models.CharField(max_length=50)
    date = models.DateField('Appointment Date', default=timezone.now())
    time = models.TimeField('Starting Appointment Time', default=timezone.now())
    endTime = models.TimeField('Ending Appointment Time', default=timezone.now() + timezone.timedelta(hours=1))
    description = models.CharField(max_length=100, default='')
    #status for seeing if app is canceled or not
    # add name field Save for R2

    def __str__(self):
        return self.location

    def has_passed(self):
        """
        Checks if the time of the appointment has passed
        :return: Boolean
        """
        return self.date <= timezone.now()

    def valid_date(self):
        """
        Check that the date of the appointment isn't in the past
        :return: Boolean
        """
        return self.date >= datetime.date(year=timezone.now().year,
                                          month=timezone.now().month,
                                          day=timezone.now().day)

    def valid_end_time(self):
        """
        Check that the end time of the appointment is after the starting time
        :return: Boolean
        """
        return self.endTime >= self.time

    def can_view(self,user):
        """
        Checks if the user is a Patient, if it is then if checks if the
        appointment belongs to that patient. If it is not a patient then the user
        can view it.
        :param user: The user trying to access the appointment
        :return: Boolean
        """
        if type(user) == Patient or type(user) == Doctor:
            return user == self.patient_ID or user == self.doctor_ID
        return True





