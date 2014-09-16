from sms.tests.config import *
from django.test import TestCase
from notifier.models import Notifier, NotifierNumber
from notifier.management.commands.notify import Command


class SendCommandTestCase(TestCase):

    def setUp(self):
        self.cron = Command()
        self.kwargs = {"model": "Notifier",
                       "notifies_left": 1,
                       "notify_text": "Foo",
                       }


    def testSetupWorks(self):
        self.assertTrue(True)

    def testBuildMessageDictBuildsDictIfNotifierHasNumbers(self):
        n = Notifier.objects.create(notify_interval=0,
                                    **self.kwargs)
        NotifierNumber.objects.create(notifier=n, phone_number="1")
        NotifierNumber.objects.create(notifier=n, phone_number="2")
        d = self.cron.build_message_dict(n)
        self.assertEqual(d, {"1": "Foo", "2": "Foo"})

    def testBuildMessageDictReturnsStringIfNoNumbers(self):
        n = Notifier.objects.create(notify_interval=0,
                                    **self.kwargs)
        d = self.cron.build_message_dict(n)
        self.assertEqual(d, "Foo")
