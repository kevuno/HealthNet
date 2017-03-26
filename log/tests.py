from django.test import TestCase
from django.utils import timezone

from .models import Entry


class LogTest(TestCase):
    def test_entry(self):
        print("-------------Testing Logs----------------")
        en = Entry(user="GOD", activity="Manually Executed Donald Trump", time=timezone.now(),
                   trigger="Outrageousness")
        self.assertEquals(en.user, "GOD", "User did not enter correctly.")
        self.assertEquals(en.activity, "Manually Executed Donald Trump", "User did not enter correctly.")
        self.assertEquals(en.time, timezone.now(), "Time did not enter correctly.")
        self.assertEquals(en.trigger, "Outrageousness", "Trigger did not enter correctly.")