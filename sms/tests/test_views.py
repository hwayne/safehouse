from os import environ

environ['MY_NUMBER'] = '6655321'
environ['TWILIO_NUMBER'] = '15005550006'
environ['DJANGO_DEBUG'] = 'True'

from unittest.mock import Mock, patch
from django.test import TestCase, Client, RequestFactory
import sms.views as view
from sms.models import Message


class SmsViewsTestCase(TestCase):

    def setUp(self):
        self.fake_num = '15005550006'
        self.request = RequestFactory()
        self.c = Client()


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

    @patch('sms.views.forward_message_to_me')
    def testTellUserIfNotFromUser(self, mock):
        self.c.post('/sms/', {'From': self.fake_num, 'Body': 'YESOCH 17'})
        mock.assert_called_with(self.fake_num, 'YESOCH 17')

    def testCreateMessageDictFromForwardingMessage(self):
        response = view.forward_message_to_me(self.fake_num, 'message')
        self.assertEqual(response[view.MY_NUMBER],
                         '{}: message'.format(self.fake_num))


class SmsRoutingTestCase(SmsViewsTestCase):

    def setUp(self):
        super().setUp()
        view.SMS_ROUTES['valid'] = Mock()
        view.SMS_ROUTES.pop('invalid', None)

    def testGetsBlackHoleIfInvalidRoute(self):
        self.c.post('/sms/', {'From': view.MY_NUMBER, 'Body': 'invalid 17'})
        pass  # no error

    def testCallsViewIfValidRoute(self):
        self.c.post('/sms/', {'From': view.MY_NUMBER, 'Body': 'valid 17'})
        view.SMS_ROUTES['valid'].assert_called()

    def testCallsViewWithParsedParameters(self):
        request = self.request.post('/sms/', {'From': view.MY_NUMBER,
                                              'Body': 'valid 17'})
        view.index(request)
        view.SMS_ROUTES['valid'].assert_called_with(request, '17')
