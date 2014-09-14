from sms.tests.config import *
from django.test import TestCase
import sms.routes as routes
from sms.routes import ROUTES
from unittest.mock import patch
from panic.models import Contact


class RoutesTestCase(TestCase):

    def testDefaultsToReflect(self):
        self.assertEqual(ROUTES['asdf'], routes.reflect)

    def testReflectCallsReflect(self):
        self.assertEqual(ROUTES['reflect'], routes.reflect)

    def testInformCallsInform(self):
        self.assertEqual(ROUTES['inform'], routes.inform)

    def testPanicCallsPanic(self):
        self.assertEqual(ROUTES['panic'], routes.panic)

    def testSayCallsSay(self):
        self.assertEqual(ROUTES['say'], routes.say)

    def testSetCallsConfig(self):
        self.assertEqual(ROUTES['set'], routes.config)

    @patch('sms.routes.config')
    def testUnsetCallsConfig(self, mock):
        return  # skip for now
        ROUTES['unset']("key")
        mock.assert_called_with("key", None)


class ReflectTestCase(TestCase):

    def testReflectTakesEmptyString(self):
        routes.reflect()  # don't break!

    def testReflectReturnsOneArgument(self):
        output = routes.reflect("asd")
        self.assertEqual("asd", output)

    def testReflectReturnsMultipleArguments(self):
        output = routes.reflect("asd", "fgh")
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

    @patch('sms.routes.forward_message_to_me')
    def testPanicBypassesMessageSaving(self, mock):
        routes.config('tag', 'abc')
        routes.panic()
        routes.process_outside_message('1234', 'this is tagged')
        mock.assert_called_with('1234', 'this is tagged')


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


class OutsideMessageTestCase(TestCase):

    @patch('sms.routes.forward_message_to_me')
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


class PopTagTestCase(TestCase):

    @patch('sms.routes.forward_message_to_me')
    def testGetsMessage(self, mock):
        routes.config('tag', 'abc')
        routes.process_outside_message('1234', 'this is tagged')
        output = routes.pop_tag('abc')
        mock.assert_called_with('1234', 'this is tagged')


class NewTemplateTestCase(TestCase):

    def testSavesTemplate(self):
        routes.make_template("a", "b")
        t = routes.model.Template.objects.get(pk=1)

    def testSavesTemplateWithName(self):
        routes.make_template("name", "b")
        t = routes.model.Template.objects.get(pk=1)
        self.assertEqual(t.name, 'name')

    def testSavesTemplateWithText(self):
        routes.make_template("a", "text")
        t = routes.model.Template.objects.get(pk=1)
        self.assertEqual(t.text, 'text')

