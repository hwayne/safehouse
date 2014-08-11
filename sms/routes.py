"""A route is a function that returns a dict consisting of
{number: message} key/values. I figured it'd be nice to keep them separate from
models, which seem strictly tied to database tables in django. The only thing
The rest of SMS should see is the ROUTES map."""

from panic.models import Contact
from sms.env import MY_NUMBER
from collections import defaultdict


def inform(*args):
    to_inform = Contact.objects.inform_all()
    return to_inform
    pass


def reflect(*args):
    """ Returns all arguments back to me as a string. Is the default. """
    return {MY_NUMBER: " ".join(args)}

ROUTES = defaultdict(lambda: reflect)
ROUTES.update({"inform": inform,
               })
