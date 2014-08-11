from django.test import TestCase
from panic.models import Contact


class ContactTestCase(TestCase):

    def setUp(self):
        self.c1 = Contact.objects.create(first_name="A1",
                                         last_name="B1",
                                         phone_number="123-456-7890",
                                         informed=True,)
        self.c2 = Contact.objects.create(first_name="A2",
                                         last_name="B2",
                                         phone_number="123-456-7891",
                                         informed=True,)


class SampleTestCase(ContactTestCase):

    def setUp(self):
        super().setUp()

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


class InformTestCase(ContactTestCase):

    def setUp(self):
        super().setUp()
        self.uninformed = Contact.objects.create(first_name="A3",
                                                 phone_number="2",
                                                 informed=False)

    def testInformAllShouldReturnUninformedPeople(self):
        informing = Contact.objects.inform_all()
        self.assertIn(self.uninformed, informing)

    def testShouldNotReturnInformedPeople(self):
        informing = Contact.objects.inform_all()
        self.assertNotIn(self.c2, informing)

    def testShouldSetUninformedToInformed(self):
        Contact.objects.inform_all()
        self.uninformed = Contact.objects.get(id=self.uninformed.id)
        self.assertTrue(self.uninformed.informed)
