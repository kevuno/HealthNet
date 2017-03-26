from django.test import TestCase
from .models import Patient
from .models import Doctor
from .models import Nurse
from .models import Hospital
from django.utils import timezone

class PatientTest(TestCase):
    def setUp(self):
        print("-------------Testing Patients----------------")
        self.patient = Patient(address="Place", city="Town", weight=50,
                               emergency_contact="Bob", emergency_number="5535545556",
                               insurance_provider="Scams R US", insurance_number=211,
                               )
        self.patient2 = Patient(address="13 America St", city="Townsville", date_of_birth=timezone.now(),
                                weight=50, phone_number="5850004444", gender="Female", height='4\'5\"',
                               emergency_contact="Rob", emergency_number="4235545559",
                               insurance_provider="Better Not", insurance_number=112,
                               )


    def test_patient_creation(self):
        self.assertTrue(self.patient.address == "Place", "Address did not enter correctly.")
        self.assertTrue(self.patient.city == "Town", "City did not enter correctly.")
        self.assertEquals(self.patient.weight, 50, "Weight did not enter correctly.")
        self.assertNotEqual(self.patient.height, None, "Height is null.")
        self.assertEqual(self.patient.height, "", "Height has a default that it shouldn't.")
        #date doesn't test because of the milisecond difference of timezone.now during runtime.
        #self.assertEqual(self.patient.date_of_birth, self.date, "Birthday is not the default.")
        self.assertEqual(self.patient.phone_number, "", "Phone number has a default when it shouldn't")
        self.assertEqual(self.patient.gender, "Male", "Gender is not the default.")

    def test_second_patient(self):
        self.assertTrue(self.patient2.address == "13 America St", "Address did not enter correctly.")
        self.assertTrue(self.patient2.city == "Townsville", "City did not enter correctly.")
        self.assertEquals(self.patient2.weight, 50, "Weight did not enter correctly.")
        self.assertEqual(self.patient2.height, "4\'5\"", "Height was not entered correctly.")
        self.assertEqual(self.patient2.gender, "Female", "Gender was misinterpreted. YIKES")
        #date doesn't test because of the milisecond difference of timezone.now during runtime.
        #self.assertEqual(self.patient2.date_of_birth, self.date, "Birthday is not the default.")
        self.assertEqual(self.patient2.phone_number, "5850004444", "Phone number was not entered correctly.")
        self.assertEqual(self.patient2.emergency_number, "4235545559", "Emergency number was not entered correctly.")
        self.assertEqual(self.patient2.emergency_contact, "Rob", "Emergency contact was not entered correctly.")
        self.assertEqual(self.patient2.insurance_number, 112, "Insurance number was not entered correctly.")
        self.assertEqual(self.patient2.insurance_provider, "Better Not", "Insurance provider was not entered correctly.")


class DoctorTest(TestCase):
    def setUp(self):
        print("-------------Testing Doctors----------------")
        self.doctor = Doctor()


    def test_doctor_creation(self):
        self.assertNotEqual(self.doctor, None, "Doctor is Null.")

class NurseTest(TestCase):
    def setUp(self):
        print("-------------Testing Nurses----------------")
        self.nurse = Nurse()


    def test_nurse_creation(self):
        self.assertNotEqual(self.nurse, None, "Nurse is Null.")

class HospitalTest(TestCase):
    def setUp(self):
        print("-------------Testing Hospitals----------------")
        self.hospital = Hospital()
        self.hospital2 = Hospital(name="Mediganja Hospital")


    def test_hospital_creation(self):
        self.assertNotEqual(self.hospital, None, "Hospital is Null.")

    def test_hospital_default(self):
        self.assertEqual(self.hospital.name, "Hospital", "Hospital default name is not hospital")

    def test_hospital(self):
        self.assertEqual(self.hospital2.name, "Mediganja Hospital", "Hospital name did not enter correctly.")