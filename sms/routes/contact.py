""" routes_contacts deals with any routes that involve sending or receiving
    messages from other people. It depends on having the 'contact'
    ('panic' in older versions) app installed.
    Has a dependency on routes.sms, which is okay because, well, you'll
    always have the sms app enabled if you're using it, right? """

from panic.models import Contact  # COUPLING
from sms.utils import get_templater
from sms.routes.sms import config, model, pop_tag

DEFAULT_MESSAGE_COUNT = 3

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


def forward_message_to_me(number, message):
    try:
        sender = Contact.objects.get(phone_number=number).full_name()
    except:
        sender = number
    return "{}: {}".format(sender, message)


def listen(tag):
    """ Given a tag, pop it and send it to you.

    In contact because it's expected these are stored people messages."""

    message = pop_tag(tag)
    return forward_message_to_me(message.phone_number, message.message)


contact_routes = {"inform": inform,
                  "panic": panic,
                  "listen": listen, # Overwrites sms listen
                  "say": say,
                  "outside": process_outside_message,
                  }

