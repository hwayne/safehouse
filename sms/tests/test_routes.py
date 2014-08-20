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
        routes.panic(10, 'lizard')
        mock.assert_called_with(10)

    @patch('sms.routes.get_templater')
    def testPanicGetsPanicMessage(self, mock):
        routes.panic()
        mock.assert_called_with('panic')

