from django.core.management.base import NoArgsCommand
from django.utils.timezone import now
from sms.models import DelayedCommand
from sms.env import MY_NUMBER
from sms.views import getsms

class Command(NoArgsCommand):
    """ Finds all delayed commands that are past due, deletes them,
    and sends them to the sms view. """

    def handle_noargs(self, **options):
        for command in DelayedCommand.objects.due_commands():
            try:
                getsms(MY_NUMBER, command.command)
                command.delete()
            except:
                pass



