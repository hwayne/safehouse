"""A route is a function that returns a dict consisting of
{number: message} key/values. I figured it'd be nice to keep them separate from
models, which seem strictly tied to database tables in django. The only thing
The rest of SMS should see is the ROUTES map."""

from panic.models import Contact  # COUPLING
from sms.utils import MY_NUMBER, get_templater
from collections import defaultdict

DEFAULT_MESSAGE_COUNT=3


def build_message_dict(contacts, template):
    return {c.phone_number:template(c) for c in contacts}


def inform(*args):
    """ Set uninformed contacts to informed and return messages for them. """
    contacts_to_inform = Contact.objects.inform_all()  # Has side effects
    return build_message_dict(contacts_to_inform, get_templater('inform'))


def panic(*args):
    """ Tell people I'm not okay. """
    try:
        count = int(args[0])
    except:
        count = DEFAULT_MESSAGE_COUNT
    contacts_to_panic = Contact.objects.sample(count)
    return build_message_dict(contacts_to_panic, get_templater('panic'))


def reflect(*args):
    """ Returns all arguments back to me as a string. Is the default. """
    return {MY_NUMBER: " ".join(args)}

ROUTES = defaultdict(lambda: reflect)
ROUTES.update({"inform": inform,
               "panic": panic,
               })