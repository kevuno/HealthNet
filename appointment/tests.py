from datetime import timedelta
from django.utils import timezone
from django.test import TestCase

from .models import Appointment


class AppointmentTests(TestCase):

    def test_valid_end_time_with_end_time_in_past(self):
        """ Test the appointment model function valid_end_time()

        :return:
        """
        start_time = timezone.now()
        end_time = timezone.now() - timezone.timedelta(hours=3)
        appointment_with_invalid_end_time = Appointment(location='Rochester', date=timezone.now(),
                                                        time=start_time, endTime=end_time)
        self.assertEqual(appointment_with_invalid_end_time.valid_end_time(), False)
        self.assertTrue(appointment_with_invalid_end_time.has_passed())

    def test_appointment_creation(self):
        apt = Appointment(location="Hell", date=(timezone.now() + timedelta(days=1)),
                time=(timezone.now() + timedelta(days=1)), endTime=((timezone.now() + timedelta(days=1, hours=1))),
                          description="This is an appointment.")
        self.assertEquals(apt.location, "Hell", "Location did not enter correctly")
        self.assertEquals(apt.date, timezone.now() + timedelta(days=1), "Date did not enter correctly")
        self.assertEquals(apt.time, timezone.now() + timedelta(days=1), "Time did not enter correctly")
        self.assertEquals(apt.endTime, timezone.now() + timedelta(days=1, hours=1), "End Time did not enter correctly")
