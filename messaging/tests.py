from django.test import TestCase
from django.utils import timezone

from .models import Message


class MessageTest(TestCase):
    def test_message(self):
        msg = Message(From="random@gmail.com", to="otherguy@yahoo.com", date=timezone.now(), time=timezone.now(),
                   subject="TEST", message="Outrageousness")
        self.assertEquals(msg.From, "random@gmail.com", "Sender email did not enter correctly.")
        self.assertEquals(msg.to, "otherguy@yahoo.com", "Recieving did not enter correctly.")
        self.assertEquals(msg.time, timezone.now(), "Time did not enter correctly.")
        self.assertEquals(msg.date, timezone.now(), "Date did not enter correctly.")
        self.assertEquals(msg.subject, "TEST", "TEST did not enter correctly.")
        self.assertEquals(msg.message, "Outrageousness", "Message did not enter correctly.")

    def test_message_defaults(self):
        msg = Message(From="d@healthnet.net", to="admin@healthnet.net")
        self.assertEquals(msg.From, "d@healthnet.net", "Sender email did not enter correctly.")
        self.assertEquals(msg.to, "admin@healthnet.net", "Recieving did not enter correctly.")
        self.assertEquals(msg.time, timezone.now(), "Default time was not timezone.now.")
        self.assertEquals(msg.date, timezone.now(), "Default date was not timezone.now.")
        self.assertEquals(msg.subject, "", "Default subject was not blank.")
        self.assertEquals(msg.message, "", "Defualt Message was not empty.")
