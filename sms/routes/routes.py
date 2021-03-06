""" A route is a function that returns a dict consisting of {number: message}
    key/values. I figured it'd be nice to keep them separate from
    models, which seem strictly tied to database tables in django. The only
    thing the rest of SMS should see is the ROUTES dispatch table.

    routes are divided into the apps they require. IE routes.contacts requires
    the panic/contacts app, routes.journal requires the journal app, etc.
    The order of import is important. Later updates clobber earlier ones,
    allowing us to define default functions in routes_base that other route
    modules can extend.

    In addition to aggregating the other apps, this file also contains routes
    that effect general use of routes, ie help and echo. """

from sms.routes.sms import sms_routes
from sms.routes.contact import contact_routes
from sms.routes.journal import journal_routes
from collections import defaultdict
from functools import partial, update_wrapper
import sms.models as model

def echo(*args):
    """ Returns all arguments back as a string. Is the default. """
    return " ".join(args)


def routes_help(route=None, routes_dict={}):
    """ Get information how the routes, either a list of all available
    routes or the docstring of a specific one. For keeping track of what
    things do.  """
    if route:
        return routes_dict[route].__doc__
    return ", ".join(sorted(routes_dict.keys()))


def default_route(routes_dict):
    """ Given a routes dict, return the function in the route with the same key
    as the value of the 'default' config. If no default, use echo."""
    try:
        default = model.Config.objects.get(key='default').val
        if default not in routes_dict.keys(): #prevent default_factory recursion
            raise KeyError
        return routes_dict[default]
    except (model.Config.DoesNotExist, KeyError):
        return echo


ROUTES = defaultdict()
ROUTES.update(sms_routes)
ROUTES.update(contact_routes)
ROUTES.update(journal_routes)
ROUTES.update({"info": update_wrapper(partial(routes_help, routes_dict=ROUTES),
                                      wrapped=routes_help),
               "echo": echo,
               })
ROUTES.default_factory = lambda: default_route(ROUTES)
