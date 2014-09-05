"""A route is a function that returns a dict consisting of
{number: message} key/values. I figured it'd be nice to keep them separate from
models, which seem strictly tied to database tables in django. The only thing
The rest of SMS should see is the ROUTES map."""

from panic.models import Contact  # COUPLING
from sms.utils import MY_NUMBER, get_templater
import sms.models as model
from collections import defaultdict
from functools import partial

DEFAULT_MESSAGE_COUNT = 3


def sms_cache(key):
    return 'sms-'+key


def build_message_dict(contacts, template):
    return {c.phone_number: template(c) for c in contacts}


def inform(*args):
    """ Set uninformed contacts to informed and return messages for them. """
    contacts_to_inform = Contact.objects.inform_all()  # Has side effects
    return build_message_dict(contacts_to_inform, get_templater('inform'))


def panic(count=DEFAULT_MESSAGE_COUNT):
    """ Tell people I'm not okay.

        Differs from say panic in that this is a hard panic, ie if the safehouse
        is in 'save messages' mode it will cancel that to ensure people can
        reach you. """

    model.config('tag', None)
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


def process_outside_message(*args):
    """ Determines whether an outsider message is stored or forwarded.

    It is stored if the user set the 'tag' cache using config.
    Otherwise, forward. """
    try:
        model.save_tagged_message(model.Config.objects.get(key='tag').val,
                                  *args)
    except model.Config.DoesNotExist:
        return forward_message_to_me(*args)
    else:
        return None


def pop_tag(tag):
    """ Given a tag, returns the oldest message with that tag.

    Note: the message is deleted by this. Not side effect free."""
    message = model.pop_message_tag(tag)
    return forward_message_to_me(message.phone_number, message.message)


def forward_message_to_me(number, message):
    try:
        sender = Contact.objects.get(phone_number=number).full_name()
    except:
        sender = number
    return {MY_NUMBER: "{}: {}".format(sender, message)}


def config(key, val):
    """ Wrapper around the config call in sms.models.

    ROUTES shouldn't have any direct connections to the model."""
    model.config(key, val)


def make_template(name, text):
    """ Saves a new template to the model.

    For on-the-fly saying. """
    model.Template.objects.create(name=name, text=text)


ROUTES = defaultdict(lambda: reflect)
ROUTES.update({"inform": inform,
               "panic": panic,
               "say": say,
               "outside": process_outside_message,
               "set": config,
               "unset": partial(config, val=None),
               "listen": pop_tag,
               "save_sms_template": make_template,
               "save-sms-template": make_template,
               })
