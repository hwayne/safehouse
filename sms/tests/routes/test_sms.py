from sms.tests.config import *
from django.test import TestCase
from datetime import timedelta
import sms.routes.sms as routes


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

class DelayTestCase(TestCase):

    def testStoresModelWithDelay(self):
        routes.delay(3, "irreverent string")
        c = routes.model.DelayedCommand.objects.get(pk=1)
        self.assertEqual((c.send_at.minute - c.created_at.minute)%60, 3)

    def testStoresModelWithCommand(self):
        routes.delay(3, "irreverent string")
        c = routes.model.DelayedCommand.objects.get(pk=1)
        self.assertEqual(c.command, "irreverent string")

    def testRecombinesCommands(self):
        routes.delay(3, "irreverent", "string")
        c = routes.model.DelayedCommand.objects.get(pk=1)
        self.assertEqual(c.command, "irreverent string")

    def testSplitsOnSemicolon(self):
        routes.delay(3, "a;b")
        c1 = routes.model.DelayedCommand.objects.get(pk=1)
        c2 = routes.model.DelayedCommand.objects.get(pk=2)
        self.assertEqual(c1.command, "a")
        self.assertEqual(c2.command, "b")

    def testStoresModelsWithSameDelay(self):
        routes.delay(3, "a;b")
        c1 = routes.model.DelayedCommand.objects.get(pk=1)
        c2 = routes.model.DelayedCommand.objects.get(pk=2)
        self.assertEqual((c1.send_at.minute - c1.created_at.minute)%60, 3)
        self.assertEqual((c2.send_at.minute - c2.created_at.minute)%60, 3)
