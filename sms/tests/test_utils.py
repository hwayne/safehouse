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
