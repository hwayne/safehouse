from django.test import TestCase
from panic.models import Contact


class ContactTestCase(TestCase):

    def setUp(self):
        Contact.objects.create(first_name="A1",
                               last_name="B1",
                               phone_number="123-456-7890",
                               informed=True,)
        Contact.objects.create(first_name="A2",
                               last_name="B2",
                               phone_number="123-456-7891",
                               informed=True,)

    def testSampleDoesntBreak(self):
        self.assertEqual(len(Contact.objects.sample(1)), 1)

    def testSampleCanTakeStrings(self):
        self.assertEqual(len(Contact.objects.sample('1')), 1)

    def testSampleHasMax(self):
        self.assertEqual(len(Contact.objects.sample(10)), 2)

    def testSampleOnlyGetsInformed(self):
        Contact.objects.create(first_name="A3",
                               last_name="B3",
                               phone_number="123-456-7891",
                               informed=False)
        self.assertEqual(len(Contact.objects.sample(10)), 2)
# Create your tests here.
