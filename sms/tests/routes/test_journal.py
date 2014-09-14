from sms.tests.config import *
from django.test import TestCase
import sms.routes.journal as routes
from journal.models import Entry

class WriteTestCase(TestCase):

    def testWritesEntry(self):
        routes.write_entry("tag")
        entry = Entry.objects.get(pk=1)
        self.assertEqual(entry.name, "tag")

    def testWritesEntryRating(self):
        routes.write_entry("tag", '3')
        entry = Entry.objects.get(pk=1)
        self.assertEqual(entry.rating, 3)

    def testWritesEntryComment(self):
        routes.write_entry("tag", '3', 'I', 'am', 'YESOCH')
        entry = Entry.objects.get(pk=1)
        self.assertEqual(entry.comment, 'I am YESOCH')

    def testOnlyWritesCommentIfCommentExists(self):
        routes.write_entry("tag")
        entry = Entry.objects.get(pk=1)
        self.assertEqual(entry.comment, None)

    def testOnlyWritesIntegerRatings(self):
        routes.write_entry("tag", 'three')
        entry = Entry.objects.get(pk=1)
        self.assertEqual(entry.rating, None)

    def testAddsStringRatingToComment(self):
        routes.write_entry("tag", 'I', 'am', 'YESOCH')
        entry = Entry.objects.get(pk=1)
        self.assertEqual(entry.comment, 'I am YESOCH')


class ReadTestCase(TestCase):

    def setUp(self):
        self.e1 = Entry.objects.create(name="bike", rating=1)
        self.e2 = Entry.objects.create(name="jog", rating=2)
        self.e3 = Entry.objects.create(name="bike", rating=3)

    def testReadsName(self):
        output = routes.read_entry("bike")
        self.assertIn("bike", output)

    def testFiltersOnName(self):
        output = routes.read_entry("jog")
        self.assertIn("jog", output)

    def testReturnsBlankIfNameNotExist(self):
        output = routes.read_entry("hike")
        self.assertEqual("", output)

    def testSortsByCreatedAt(self):
        output = routes.read_entry("bike")
        self.assertIn("3", output)

    def testGetSecondMostRecent(self):
        output = routes.read_entry("bike", 2)
        self.assertIn("1", output)

    def testDoesNotAcceptNegativeNumbers(self):
        output = routes.read_entry("bike", -2)
        self.assertIn("3", output)
