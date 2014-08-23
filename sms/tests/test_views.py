from sms.tests.config import *
from unittest.mock import Mock, patch
from django.test import TestCase, Client, RequestFactory
import sms.views as view
from sms.models import Message


class SmsViewsTestCase(TestCase):

    def setUp(self):
        self.fake_num = '15005550006'
        self.request = RequestFactory()
        self.c = Client()
        view.sendsms = Mock(return_value=view.HttpResponse("Test"))


class SmsLoggingTestCase(SmsViewsTestCase):

    def setup(self):
        super().setUp()

    def testLogMessageIfNotFromUserNumber(self):
        self.c.post('/sms/', {'From': self.fake_num})
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get(pk=1).phone_number, self.fake_num)

    def testGetBodyIfMessageLogged(self):
        self.c.post('/sms/', {'From': self.fake_num, 'Body': 'YESOCH'})
        self.assertEqual(Message.objects.get(pk=1).message, 'YESOCH')

    def testLogMessageIfInvalidRoute(self):
        self.c.post('/sms/', {'From': view.MY_NUMBER, 'Body': 'YESOCH 17'})
        self.assertEqual(Message.objects.get(pk=1).message, 'YESOCH 17')

    @patch('sms.views.ROUTES')
    def testTellUserIfNotFromUser(self, mock):
        self.c.post('/sms/', {'From': self.fake_num, 'Body': 'YESOCH 17'})
        mock['forward'].assert_called_with(self.fake_num, 'YESOCH 17')


class SmsRoutingTestCase(SmsViewsTestCase):

    def setUp(self):
        super().setUp()
        view.ROUTES['valid'] = Mock()
        view.ROUTES.pop('invalid', None)

    def testGetsBlackHoleIfInvalidRoute(self):
        self.c.post('/sms/', {'From': view.MY_NUMBER, 'Body': 'invalid 17'})
        pass  # no error

    def testCallsViewIfValidRoute(self):
        self.c.post('/sms/', {'From': view.MY_NUMBER, 'Body': 'valid 17'})
        view.ROUTES['valid'].assert_called()

    def testCallsViewWithParsedParameters(self):
        request = self.request.post('/sms/', {'From': view.MY_NUMBER,
                                              'Body': 'valid 17'})
        view.index(request)
        view.ROUTES['valid'].assert_called_with('17')
