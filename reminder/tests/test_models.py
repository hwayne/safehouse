from django.test import TestCase
from django.db import models
from reminder.models import Reminder, get_date, get_date_method
from datetime import date, timedelta


class ReminderTestCase(TestCase):

    def setUp(self):
        # Should be a global
        # We test Reminder ON ITSELF (crazy sounds)

        self.kwargs = {"model": "Reminder",
                       "reminder_interval": 2,
                       "reminders_left": 2,
                       }
        self.test_list = []
        for i in range(2):
            r = Reminder.objects.create(reminder_text=str(i),
                                        **self.kwargs)
            r.created_at = date.today() - timedelta(days=i)
            r.save()
            self.test_list.append(r)


class ReminderValidationTestCase(ReminderTestCase):

    def setUp(self):
        super().setUp()


class ReminderQueryingTestCase(ReminderTestCase):

    def setUp(self):
        super().setUp()
        self.kwargs['reminder_text'] = "Test"

    def testCanGetModel(self):
        r = Reminder.objects.create(**self.kwargs)
        model = r.get_model_class()
        self.assertIs(model, Reminder)

    def testCanGetModelClassTimeMethod(self):
        self.assertEqual(get_date_method(Reminder), 'created_at')

    def testCanGetModelCreatedAt(self):
        for r in self.test_list:
            self.assertEqual(r.created_at, get_date(r, 'created_at'))

    def testGetsMostRecentIfNoColumnVal(self):
        r = Reminder.objects.create(**self.kwargs)
        model = r.get_most_recent_model('created_at')
        self.assertEqual(self.test_list[0], model)

    def testGetsMostRecentWithColumnVal(self):
        r = Reminder.objects.create(column="reminder_text",
                                    column_val="1",
                                    **self.kwargs)

        model = r.get_most_recent_model('created_at')
        self.assertEqual(self.test_list[1], model)


class ReminderCanRemindTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.mock_kwargs = {"model": "Reminder",
                            "reminder_text": "Test",
                            "reminder_interval": 2,
                            "reminders_left": 2,
                            }

        self.kwargs = {"model": "Reminder",
                       "reminder_text": "Test",
                       }

    def testCanRemind(self):
        r = Reminder.objects.create(reminder_interval=0,
                                    reminders_left=2,
                                    **self.kwargs
                                    )
        self.assertTrue(r.can_remind())

    def testCannotRemindIfOut(self):
        r = Reminder.objects.create(reminder_interval=0,
                                    reminders_left=0,
                                    **self.kwargs
                                    )
        self.assertFalse(r.can_remind())

    def testCannotRemindIfTooEarly(self):
        r = Reminder.objects.create(reminder_interval=1,
                                    reminders_left=1,
                                    **self.kwargs
                                    )
        self.assertFalse(r.can_remind())
