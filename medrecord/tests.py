from django.test import TestCase
from .models import MedicalRecord
from .models import Prescription
from .models import TestResult

class MedRecordTest(TestCase):
    def setUp(self):
        print("-------------Testing Med Records----------------")
        self.med = MedicalRecord(title="Record")

    def test_MedRecord(self):
        self.assertEqual(self.med.title, "Record", "Title did not enter correctly.")
        self.assertEqual(self.med.file, None, "Magical file found.")
        #self.assertEqual(self.med.date, timezone.localtime(timezone.now()), "Date did not enter correctly.")
        self.assertEqual(self.med.patient_ID, 1, "Patient ID did not enter correctly.")

class PrescriptionTest(TestCase):
    def setUp(self):
        print("-------------Testing Prescriptions----------------")

        self.drugs = Prescription(medication="Mariganja Tincture", dosage="1000",
                                  description="Syrup for my pancakes", quantity="365")

    def test_Prescriptions(self):
        self.assertEqual(self.drugs.patient, 1, "Patient did not enter correctly.")
        self.assertEqual(self.drugs.medication, "Mariganja Tincture", "Medication did not enter correctly.")
        self.assertEqual(self.drugs.dosage, "1000", "Dosage did not enter correctly.")
        self.assertEqual(self.drugs.description, "Syrup for my pancakes", "Description did not enter correctly.")
        self.assertEqual(self.drugs.quantity, "365", "Quantity did not enter correctly.")


class TestResultTest(TestCase):
    def setUp(self):
        print("-------------Testing Test Results----------------")
        self.test = TestResult(description="AIDS TEST", released=False)

    def test_Tests(self):
        self.assertEqual(self.test.description, "AIDS TEST", "Description did not enter correctly.")
        self.assertEqual(self.test.released, False, "Test released itself.")
        self.assertEqual(self.test.comment, None, "Comment not null by default.")
