""" routes_base deals with any commands that affect the server or how the sms
app functions. It does not depend on having other apps installed. """

from functools import partial
import sms.models as model

def config(key, val):
    """ Wrapper around the config call in sms.models.

    ROUTES shouldn't have any direct connections to the model."""
    model.config(key, val)


def pop_tag(tag):
    """ Given a tag, returns the oldest message with that tag.

    Note: the message is deleted by this. Not side effect free."""
    message = model.pop_message_tag(tag)
    return message #forward_message_to_me(message.phone_number, message.message)


def make_template(name, text):
    """ Saves a new template to the model.

    For on-the-fly saying. """
    model.Template.objects.create(name=name, text=text)


sms_routes = {"set": config,
               "unset": partial(config, val=None),
               "listen": lambda x: str(pop_tag(x)),
               "save_sms_template": make_template,
               "save-sms-template": make_template,
               }
