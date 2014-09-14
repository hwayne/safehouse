from sms.tests.config import *
from django.test import TestCase
from sms.routes.routes import ROUTES
import sms.routes.routes as routes


class ReflectTestCase(TestCase):

    def testReflectTakesEmptyString(self):
        routes.reflect()  # don't break!

    def testReflectReturnsOneArgument(self):
        output = routes.reflect("asd")
        self.assertEqual("asd", output)

    def testReflectReturnsMultipleArguments(self):
        output = routes.reflect("asd", "fgh")
        self.assertEqual("asd fgh", output)


class HelpTestCase(TestCase):

    def testGetsAvailableCommands(self):
        output = routes.routes_help(None, {"a": "b", "c": "d"})
        self.assertIn('a', output)
        self.assertIn('c', output)

    def testAddingCommandGetsDocString(self):
        output = routes.routes_help('help', ROUTES)
        self.assertIn("docstring", output)

class RoutesTestCase(TestCase):

    def testDefaultsToReflect(self):
        self.assertEqual(ROUTES['asdf'], routes.reflect)

    def testCanCallHelp(self):
        ROUTES['help']("route")

    #def testReflectCallsReflect(self):
        #self.assertEqual(ROUTES['reflect'], routes.reflect)

    #def testInformCallsInform(self):
        #self.assertEqual(ROUTES['inform'], routes.inform)

    #def testPanicCallsPanic(self):
        #self.assertEqual(ROUTES['panic'], routes.panic)

    #def testSayCallsSay(self):
        #self.assertEqual(ROUTES['say'], routes.say)

    #def testSetCallsConfig(self):
        #self.assertEqual(ROUTES['set'], routes.config)

    #@patch('sms.routes.config')
    #def testUnsetCallsConfig(self, mock):
        #return  # skip for now
        #ROUTES['unset']("key")
        #mock.assert_called_with("key", None)





