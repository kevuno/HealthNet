from django.test import TestCase

from django.test import TestCase
from appointment.models import Appointment
from userprofile.models import Patient
from django.utils import timezone


# Create your tests here.
# Not very valuable. Tests will be run manually for now.

class PatientTest(TestCase):
    def setUp(self):
        p1 = Patient(address="Place", city="Town", weight=50,
                               emergency_contact="Bob", emergency_number="5535545556",
                               insurance_provider="Scams R US", insurance_number=211,
                               )
        p2 = Patient(address="Place2", city="City2", weight=100,
                               emergency_contact="John", emergency_number="5535549556",
                               insurance_provider="DeathProfits", insurance_number=2311,
                               )
'''
class AppointmentTest(TestCase):
    def setUp(self):
        Appointment.objects.create(patient_ID="1",
                                   doctor_ID="1", location="Room 15",
                                   date=(timezone.now() - timezone.timedelta(days=1)), time=timezone.now,
                                   endTime=timezone.now,
                                   description="Testing Appointments")
        Appointment.objects.create(patient_ID="2",
                                   doctor_ID="2", location="Room 25",
                                   date=timezone.now, time=timezone.now,
                                   endTime=(timezone.now() - timezone.timedelta(hours=2)),
                                   description="Testing Appointments 2")

    def test_appointments(self):
        a1 = Appointment.objects.get(patient_ID="1")
        a2 = Appointment.objects.get(patient_ID="1")

        self.assertTrue(a1.has_passed())
        self.assertFalse(a2.has_passed())
        self.assertFalse(a2.valid_end_time())
        self.assertTrue(a1.valid_end_time())
'''
