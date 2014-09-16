from django.core.management.base import NoArgsCommand
from notifier.models import Notifier
from sms.views import sendsms # OH NO COUPLING

class Command(NoArgsCommand):
    """ Finds all notifications that can be sent out, updates them,
    and sends them out.

    This will only send notifications that haven't been triggered recently.
    See the Notifier manager for more details. """

    def build_message_dict(self, notifier):
        """ Given a Notifier model, returns a dict with keys of the phone numbers
        of the related NotifierNumbers, and values of the notification.

        If no such numbers exist, we are supposed to send it to ourselves, so
        we just return a string for the sms app. """

        numbers = notifier.notifiernumber_set.all()
        if numbers:
            return {n.phone_number: notifier.notify_text for n in numbers}
        else:
            return notifier.notify_text

    def handle_noargs(self, **options):
        for notifier in Notifier.objects.due_notifications():
            notifier.notifies_left -= 1
            notifier.save()
            sendsms(self.build_message_dict(notifier))

