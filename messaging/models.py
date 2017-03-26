from django.db import models
from django.utils import timezone
from userprofile.models import Patient, Doctor, Nurse


# Create your models here.
class Message(models.Model):
    From = models.EmailField(max_length=50, default="")
    to = models.EmailField(max_length=50, default="")
    date = models.DateField("Date", default=timezone.now())
    time = models.TimeField("Time", default=timezone.now())
    subject = models.CharField(max_length=100, default="")
    message = models.TextField(max_length=500, default="")