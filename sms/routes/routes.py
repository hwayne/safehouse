""" A route is a function that returns a dict consisting of {number: message}
    key/values. I figured it'd be nice to keep them separate from
    models, which seem strictly tied to database tables in django. The only thing
    The rest of SMS should see is the ROUTES map.

    routes are divided into the apps they require. IE routes_contacts requires
    the panic/contacts app, routes_journal requires the journal app, etc.
    The order of import is important. Later updates clobber earlier ones,
    allowing us to define default functions in routes_base that other route
    modules can extend.

    """
from sms.routes.sms import sms_routes, reflect
from sms.routes.contact import contact_routes
from collections import defaultdict

ROUTES = defaultdict(lambda: reflect)
ROUTES.update(sms_routes)
ROUTES.update(contact_routes)
