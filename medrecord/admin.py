from django.contrib import admin
from .models import MedicalRecord, TestResult, Prescription

# Register your models here.
admin.site.register(MedicalRecord)
admin.site.register(TestResult)
admin.site.register(Prescription)