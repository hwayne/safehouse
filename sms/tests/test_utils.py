from sms.tests.config import *
from django.test import TestCase
import sms.utils as util


class CleanNumberTestCase(TestCase):

    def testCleanNumberLeavesNumbers(self):
        self.assertEqual('12345', util.clean_number('12345'))

    def testCleanNumberRemovesNonnumbers(self):
        self.assertEqual('12345', util.clean_number('a+1aszz23!!!45'))


class SmsParserTestCase(TestCase):

    def setUp(self):
        pass

    def testSmsGetsRoute(self):
        output = util.parse_message("yesoch knows all")
        self.assertEqual(output['route'], 'yesoch')

    def testSmsLowerCasesStuff(self):
        output = util.parse_message("YESOCH knows all")
        self.assertEqual(output['route'], 'yesoch')

    def testSmsGetsArguments(self):
        output = util.parse_message("YESOCH knows all")
        self.assertEqual(output['args'], ['knows', 'all'])


from sms.models import Template
from panic.models import Contact
class GetTemplaterTestCase(TestCase):

    def setUp(self):
        self.contact = Contact.objects.create(first_name="a")

    def testDefaultsToDjangoTemplates(self):
        t2 = Template.objects.create(name="panic", text="test")
        template = util.get_templater("panic")(self.contact)
        self.assertNotIn("test", template)

    def testThenTriesModelTemplates(self):
        t2 = Template.objects.create(name="test", text="a test")
        template = util.get_templater("test")(self.contact)
        self.assertIn("a test", template)
