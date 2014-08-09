from django.test import TestCase, RequestFactory  # , Client
import panic.views as view
from panic.models import Contact


class PanicViewsTestCase(TestCase):

  def setUp(self):
      self.contact = Contact.objects.create(first_name="A1",
                                            phone_number="2",
                                            informed=True)
      self.request = RequestFactory()

# Random stuff

  def testRandomReturnsHTML(self):
      request = self.request.post('/', CONTENT_TYPE="application/html")
      response = view.random(request)
      self.assertIn('html', response['content-type'])

  def testRandomReturnsInternal(self):
      request = self.request.post('/', CONTENT_TYPE="internal")
      response = view.random(request)
      self.assertEqual(type(response), dict)

  def testInternalHasNumbersAsKeys(self):
      number = Contact.objects.get(pk=1).phone_number
      request = self.request.post('/', CONTENT_TYPE="internal")
      response = view.random(request)
      self.assertEqual(list(response.keys()), [number])

  def testInternalHasTemplateAsValues(self):
      request = self.request.post('/', CONTENT_TYPE="internal")
      response = view.random(request)
      text = response[self.contact.phone_number]
      self.assertIn(self.contact.first_name, text)


class InformTestCase(PanicViewsTestCase):

    def setUp(self):
        super().setUp()
        self.uninformed = Contact.objects.create(first_name="A2",
                                                 phone_number="2",
                                                 informed=False)


    def testInformDoesNothingIfNoUninformed(self):
        request = self.request.post('/', CONTENT_TYPE="internal")
        response = view.inform(request)
        response = view.inform(request)
        self.assertEqual(b"No Uninformed", response.content)

    def testInformOnlyGetsUninformed(self):
        request = self.request.post('/', CONTENT_TYPE="internal")
        response = view.inform(request)
        self.assertEqual(len(response), 1)
        self.assertIn(self.uninformed.phone_number, response)

    def testInformSetsPeopleToInformed(self):
        request = self.request.post('/', CONTENT_TYPE="internal")
        response = view.inform(request)
        self.uninformed = Contact.objects.get(id=self.uninformed.id)
        self.assertTrue(self.uninformed.informed)
