from django.contrib import admin
from .models import Doctor, Patient, Nurse, Hospital
# Register your models here.
admin.site.register(Nurse)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Hospital)
