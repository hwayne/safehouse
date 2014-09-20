from django.test import TestCase
from django.db import models
from notifier.models import Notifier, get_date_method
from datetime import datetime, timedelta


class NotifierTestCase(TestCase):

    def setUp(self):
        # Should be a global
        # We test Notifier ON ITSELF (crazy sounds)

        self.kwargs = {"model": "Notifier",
                       "notify_interval": 2,
                       "notifies_left": 2,
                       }
        self.test_list = []
        for i in range(2):
            r = Notifier.objects.create(notify_text=str(i),
                                        **self.kwargs)
            r.created_at -= timedelta(days=i)
            r.save()
            self.test_list.append(r)


class NotifierValidationTestCase(NotifierTestCase):

    def setUp(self):
        super().setUp()


class NotifierQueryingTestCase(NotifierTestCase):

    def setUp(self):
        super().setUp()
        self.kwargs['notify_text'] = "Test"

    def testCanGetModel(self):
        r = Notifier.objects.create(**self.kwargs)
        model = r.get_model_class()
        self.assertIs(model, Notifier)

    def testCanGetModelClassTimeMethod(self):
        self.assertEqual(get_date_method(Notifier), 'created_at')

    def testGetsMostRecentIfNoColumnVal(self):
        model = self.test_list[1].get_most_recent_model('created_at')
        self.assertEqual(self.test_list[0], model)

    def testGetsMostRecentWithColumnVal(self):
        r = Notifier.objects.create(column="notify_text",
                                    column_val="1",
                                    **self.kwargs)

        model = r.get_most_recent_model('created_at')
        self.assertEqual(self.test_list[1], model)


class NotifierCanNotifyTestCase(TestCase):

    def setUp(self):
        self.mock_kwargs = {"model": "Notifier",
                            "notify_text": "Test",
                            "notify_interval": 2,
                            "notifies_left": 2,
                            }

        self.kwargs = {"model": "Notifier",
                       "notify_text": "Test",
                       }

    def testCanNotify(self):
        r = Notifier.objects.create(notify_interval=0,
                                    notifies_left=2,
                                    **self.kwargs
                                    )
        self.assertTrue(r.can_notify())

    def testCannotNotifyIfOut(self):
        r = Notifier.objects.create(notify_interval=0,
                                    notifies_left=0,
                                    **self.kwargs
                                    )
        self.assertFalse(r.can_notify())

    def testCannotNotifyIfTooEarly(self):
        r = Notifier.objects.create(notify_interval=1,
                                    notifies_left=1,
                                    **self.kwargs
                                    )
        self.assertFalse(r.can_notify())

    def testCannotNotifyIfInvalid(self):
        n = Notifier.objects.create(notify_interval=0,
                                    column="oogly",
                                    column_val="boogly",
                                    notifies_left=2,
                                    **self.kwargs)
        self.assertFalse(n.can_notify())

    def testCannotnotifyIfColumnValMissing(self):
        n = Notifier.objects.create(notify_interval=0,
                                    column="column",
                                    column_val="boogly",
                                    notifies_left=2,
                                    **self.kwargs)
        self.assertFalse(n.can_notify())

class NotifierManagerTestCase(TestCase):

    def setUp(self):
        self.kwargs = {"model": "Notifier",
                       "notifies_left": 1,
                       "notify_text": "Foo",
                       }

    def testGetDueNotificationsGetsDue(self):
        n = Notifier.objects.create(notify_interval=0,
                                    **self.kwargs)
        notifiers = Notifier.objects.due_notifications()
        self.assertIn(n, notifiers)


    def testGetDueNotificationsNotGetNotDue(self):
        n = Notifier.objects.create(notify_interval=1,
                                    **self.kwargs)
        notifiers = Notifier.objects.due_notifications()
        self.assertNotIn(n, notifiers)

    def testDoesNotGetNotificationsUpdatedWithinInterval(self):
        n = Notifier.objects.create(notify_interval=5,
                                    **self.kwargs)
        n.created_at -= timedelta(days=10)
        n.save() # Makes updated_at NOW
        notifiers = Notifier.objects.due_notifications()
        self.assertNotIn(n, notifiers)

