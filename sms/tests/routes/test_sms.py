from sms.tests.config import *
from django.test import TestCase
import sms.routes.sms as routes


class ReflectTestCase(TestCase):

    def testReflectTakesEmptyString(self):
        routes.reflect()  # don't break!

    def testReflectReturnsOneArgument(self):
        output = routes.reflect("asd")
        self.assertEqual("asd", output)

    def testReflectReturnsMultipleArguments(self):
        output = routes.reflect("asd", "fgh")
        self.assertEqual("asd fgh", output)

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

