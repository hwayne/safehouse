from sms.tests.config import *
from django.test import TestCase
from sms.routes.routes import ROUTES
import sms.routes.routes as routes


class EchoTestCase(TestCase):

    def testEchoTakesEmptyString(self):
        routes.echo()  # don't break!

    def testEchoReturnsOneArgument(self):
        output = routes.echo("asd")
        self.assertEqual("asd", output)

    def testEchoReturnsMultipleArguments(self):
        output = routes.echo("asd", "fgh")
        self.assertEqual("asd fgh", output)


class HelpTestCase(TestCase):

    def testGetsAvailableCommands(self):
        output = routes.routes_help(None, {"a": "b", "c": "d"})
        self.assertIn('a', output)
        self.assertIn('c', output)

    def testAddingCommandGetsDocString(self):
        output = routes.routes_help('info', ROUTES)
        self.assertIn("docstring", output)

class RoutesTestCase(TestCase):

    def testDefaultsToEcho(self):
        self.assertEqual(ROUTES['asdf'], routes.echo)

    def testCanCallHelp(self):
        ROUTES['help']("route")

    #def testEchoCallsecho(self):
        #self.assertEqual(ROUTES['echo'], routes.reflect)

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





