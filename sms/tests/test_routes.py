from sms.tests.config import *
from django.test import TestCase
import sms.routes as routes
from sms.routes import ROUTES
from unittest.mock import patch
from panic.models import Contact
routes.MY_NUMBER = "0"


class RoutesTestCase(TestCase):

    def testDefaultsToReflect(self):
        self.assertEqual(ROUTES['asdf'], routes.reflect)

    def testCallsReflect(self):
        self.assertEqual(ROUTES['reflect'], routes.reflect)

    def testCallsInform(self):
        self.assertEqual(ROUTES['inform'], routes.inform)

    def testCallsPanic(self):
        self.assertEqual(ROUTES['panic'], routes.panic)

    def testCallsSay(self):
        self.assertEqual(ROUTES['say'], routes.say)

    def testCallsForward(self):
        self.assertEqual(ROUTES['forward'], routes.forward_message_to_me)


class ReflectTestCase(TestCase):

    def testReflectTakesEmptyString(self):
        routes.reflect()  # don't break!

    def testReflectReturnsMyNumber(self):
        output = routes.reflect("asdasd")
        self.assertIn(routes.MY_NUMBER, output)

    def testReflectReturnsOneArgument(self):
        output = routes.reflect("asd")[routes.MY_NUMBER]
        self.assertEqual("asd", output)

    def testReflectReturnsMultipleArguments(self):
        output = routes.reflect("asd", "fgh")[routes.MY_NUMBER]
        self.assertEqual("asd fgh", output)


class InformTestCase(TestCase):

    def setUp(self):
        self.c = Contact.objects.create(phone_number="666",
                                        informed=False)

    @patch('sms.routes.Contact.objects.inform_all')
    def testInformCallsInformAll(self, mock):
        routes.inform()
        mock.assert_called_with()

    def testInformReturnsDict(self):
        self.assertIsInstance(routes.inform(), dict)

    def testInformKeyIsNumber(self):
        self.assertIn(self.c.phone_number, routes.inform().keys())

    @patch('sms.routes.get_templater')
    def testInformGetsInformMessage(self, mock):
        routes.inform()
        mock.assert_called_with('inform')


class PanicTestCase(TestCase):

    @patch('sms.routes.Contact.objects.sample')
    def testPanicCallsSampleWithDefaultCount(self, mock):
        routes.panic()
        mock.assert_called_with(routes.DEFAULT_MESSAGE_COUNT)

    @patch('sms.routes.Contact.objects.sample')
    def testPanicCallsSampleWithCount(self, mock):
        routes.panic(10)
        mock.assert_called_with(10)

    @patch('sms.routes.get_templater')
    def testPanicGetsPanicMessage(self, mock):
        routes.panic()
        mock.assert_called_with('panic')


class SayTestCase(TestCase):

    @patch('sms.routes.get_templater')
    @patch('sms.routes.Contact.objects.sample')
    def testSayHasDefaultParams(self, mock_sample, mock_template):
        routes.say()
        mock_sample.assert_called_with(routes.DEFAULT_MESSAGE_COUNT)
        mock_template.assert_called_with('talk')

    @patch('sms.routes.get_templater')
    @patch('sms.routes.Contact.objects.sample')
    def testSayHasCallableParams(self, mock_sample, mock_template):
        routes.say('YESOCH', 10)
        mock_sample.assert_called_with(10)
        mock_template.assert_called_with('yesoch')

class ForwardTestCase(TestCase):

    def setUp(self):
        self.c = Contact.objects.create(phone_number="123",
                                        first_name="A",
                                        last_name="B",
                                        informed=False)

    def testGetsNameIfInDatabase(self):
        response = routes.forward_message_to_me("123", "My name's YESOCH")
        self.assertIn("A", response[routes.MY_NUMBER])
        self.assertIn("B", response[routes.MY_NUMBER])

    def testGetsNumberIfNotInDatabase(self):
        response = routes.forward_message_to_me("1234", "My name's YESOCH")
        self.assertIn("1234", response[routes.MY_NUMBER])

    def testGetsMessage(self):
        response = routes.forward_message_to_me("123", "My name's YESOCH")
        self.assertIn("My name's YESOCH", response[routes.MY_NUMBER])
