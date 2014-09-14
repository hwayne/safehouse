from sms.tests.config import *
from django.test import TestCase
from unittest.mock import patch
import sms.routes.contact as routes
from panic.models import Contact

SAMPLE = 'sms.routes.contact.Contact.objects.sample'
INFORM_ALL = 'sms.routes.contact.Contact.objects.inform_all'
GET_TEMPLATER = 'sms.routes.contact.get_templater'
FORWARD_TO_ME = 'sms.routes.contact.forward_message_to_me'


class InformTestCase(TestCase):

    def setUp(self):
        self.c = Contact.objects.create(phone_number="666",
                                        informed=False)

    @patch(INFORM_ALL)
    def testInformCallsInformAll(self, mock):
        routes.inform()
        mock.assert_called_with()

    def testInformReturnsDict(self):
        self.assertIsInstance(routes.inform(), dict)

    def testInformKeyIsNumber(self):
        self.assertIn(self.c.phone_number, routes.inform().keys())

    @patch(GET_TEMPLATER)
    def testInformGetsInformMessage(self, mock):
        routes.inform()
        mock.assert_called_with('inform')


class PanicTestCase(TestCase):

    @patch(SAMPLE)
    def testPanicCallsSampleWithDefaultCount(self, mock):
        routes.panic()
        mock.assert_called_with(routes.DEFAULT_MESSAGE_COUNT)

    @patch(SAMPLE)
    def testPanicCallsSampleWithCount(self, mock):
        routes.panic(10)
        mock.assert_called_with(10)

    @patch(GET_TEMPLATER)
    def testPanicGetsPanicMessage(self, mock):
        routes.panic()
        mock.assert_called_with('panic')

    @patch(FORWARD_TO_ME)
    def testPanicBypassesMessageSaving(self, mock):
        routes.config('tag', 'abc')
        routes.panic()
        routes.process_outside_message('1234', 'this is tagged')
        mock.assert_called_with('1234', 'this is tagged')


class SayTestCase(TestCase):

    @patch(GET_TEMPLATER)
    @patch(SAMPLE)
    def testSayHasDefaultParams(self, mock_sample, mock_template):
        routes.say()
        mock_sample.assert_called_with(routes.DEFAULT_MESSAGE_COUNT)
        mock_template.assert_called_with('talk')

    @patch(GET_TEMPLATER)
    @patch(SAMPLE)
    def testSayHasCallableParams(self, mock_sample, mock_template):
        routes.say('YESOCH', 10)
        mock_sample.assert_called_with(10)
        mock_template.assert_called_with('yesoch')


class OutsideMessageTestCase(TestCase):

    @patch(FORWARD_TO_ME)
    def testCallsForwardIfNoTagCache(self, mock):
        routes.process_outside_message("123", "Hail YESOCH")
        mock.assert_called_with("123", "Hail YESOCH")

    @patch('sms.models.save_tagged_message')
    def testCallsStoreIfTagCache(self, mock):
        routes.config('tag', 'elephant')
        routes.process_outside_message("123", "Hail YESOCH")
        mock.assert_called_with("elephant", '123', "Hail YESOCH")


class ForwardTestCase(TestCase):

    def setUp(self):
        self.c = Contact.objects.create(phone_number="123",
                                        first_name="A",
                                        last_name="B",
                                        informed=False)

    def testGetsNameIfInDatabase(self):
        response = routes.forward_message_to_me("123", "My name's YESOCH")
        self.assertIn("A", response)
        self.assertIn("B", response)

    def testGetsNumberIfNotInDatabase(self):
        response = routes.forward_message_to_me("1234", "My name's YESOCH")
        self.assertIn("1234", response)

    def testGetsMessage(self):
        response = routes.forward_message_to_me("123", "My name's YESOCH")
        self.assertIn("My name's YESOCH", response)


class ListenTestCase(TestCase):

    @patch(FORWARD_TO_ME)
    def testGetsMessage(self, mock):
        routes.config('tag', 'abc')
        routes.process_outside_message('1234', 'this is tagged')
        output = routes.listen('abc')
        mock.assert_called_with('1234', 'this is tagged')
