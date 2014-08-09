from os import environ
from django.views.decorators.csrf import csrf_exempt
from safehouse.settings import DEBUG
from safehouse.internal_routes import SMS_ROUTES

# we know they're ok, since it's an internal route
for key, item in SMS_ROUTES.items():
    wrapped_item = csrf_exempt(SMS_ROUTES[key])
    SMS_ROUTES[key] = wrapped_item

# For debugging 'n stuff MOVE THIS
def reflect(request, *args):
    return {MY_NUMBER: " ".join(args)}

SMS_ROUTES['reflect'] = reflect

MY_NUMBER = environ['MY_NUMBER']
TWILIO_NUMBER = environ['TWILIO_NUMBER']
