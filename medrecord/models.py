from django.db import models
from django.utils import timezone
from userprofile.models import Doctor, Patient
from django.core.validators import RegexValidator

# TODO do files have patients and doctors or vise versa
class MedicalRecord(models.Model):
    title = models.CharField(max_length=50, null=True)
    file = models.FileField(upload_to='medical_records/%Y/%m/%d/', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now(), editable=False)
    patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
    # doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

# TODO: don't have prescription inherit from MedicalRecord
class Prescription(MedicalRecord):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
    medication = models.CharField(max_length=100, default='')
    dosage = models.CharField(validators=[RegexValidator(regex='^[1-9][0-9]*\s?(mg|mL)$',
                                                         message='Quantity should be greater than 0 mg/mL and specify mg or mL')],
                              max_length=50, null=True, verbose_name='Quantity(mg or mL[for liquids])')
    description = models.CharField(max_length=100, null=True)
    quantity = models.CharField(validators=[RegexValidator(regex='^[1-9][0-9]*$', message='Dosage should be greater than 0 doses')],
                                max_length=100, null=True, verbose_name='Dosage(Doses)')



class TestResult(MedicalRecord):
    description = models.CharField(max_length=200, null=True)
    released = models.BooleanField(default=True)
    comment = models.CharField(max_length=200, null=True)