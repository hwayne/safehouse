from django.test import TestCase
import sms.routes as routes
from sms.routes import ROUTES
from unittest.mock import patch
routes.MY_NUMBER = "0"


class RoutesTestCase(TestCase):

    def testDefaultsToReflect(self):
        self.assertEqual(ROUTES['asdf'], routes.reflect)

    def testCallsReflect(self):
        self.assertEqual(ROUTES['reflect'], routes.reflect)

    def testCallsInform(self):
        self.assertEqual(ROUTES['inform'], routes.inform)


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

    @patch('sms.routes.Contact.objects.inform_all')
    def testInformCallsInformAll(self, mock):
        routes.inform()
        mock.assert_called_with()
