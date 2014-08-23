"""A route is a function that returns a dict consisting of
{number: message} key/values. I figured it'd be nice to keep them separate from
models, which seem strictly tied to database tables in django. The only thing
The rest of SMS should see is the ROUTES map."""

from panic.models import Contact  # COUPLING
from sms.utils import MY_NUMBER, get_templater
from collections import defaultdict

DEFAULT_MESSAGE_COUNT = 3


def build_message_dict(contacts, template):
    return {c.phone_number: template(c) for c in contacts}


def inform(*args):
    """ Set uninformed contacts to informed and return messages for them. """
    contacts_to_inform = Contact.objects.inform_all()  # Has side effects
    return build_message_dict(contacts_to_inform, get_templater('inform'))


def panic(count=DEFAULT_MESSAGE_COUNT):
    """ say people I'm not okay.

        Takes a count."""

    contacts_to_panic = Contact.objects.sample(count)
    return build_message_dict(contacts_to_panic, get_templater('panic'))


def say(template="talk", count=DEFAULT_MESSAGE_COUNT):
    """ Arbitrary template finder and messager.

        Takes a template name, count, outputs dict. """

    contacts_to_say = Contact.objects.sample(count)
    return build_message_dict(contacts_to_say, get_templater(template.lower()))


def reflect(*args):
    """ Returns all arguments back to me as a string. Is the default. """
    return {MY_NUMBER: " ".join(args)}


def forward_message_to_me(number, message):
    try:
        sender = Contact.objects.get(phone_number=number).full_name()
    except:
        sender = number
    return {MY_NUMBER: "{}: {}".format(sender, message)}


ROUTES = defaultdict(lambda: reflect)
ROUTES.update({"inform": inform,
               "panic": panic,
               "say": say,
               "forward": forward_message_to_me,
               })
