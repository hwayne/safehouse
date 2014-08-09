# from django.shortcuts import render
from django.http import HttpResponse
from sms.env import MY_NUMBER, TWILIO_NUMBER, DEBUG, SMS_ROUTES
from django_twilio.decorators import twilio_view
from django_twilio.client import twilio_client
from sms.utils import parse_message, clean_number, log_message

# from twilio.twiml import Response
# from django.template import RequestContext, loader



@twilio_view
def index(request):
    from_number = clean_number(request.POST.get('From', '0'))
    message = request.POST.get('Body', '')
    #log_message(from_number, request.build_absolute_uri())
    log_message(from_number, message)  # for posterity!

    request.META['CONTENT_TYPE'] = 'internal'  # BAM

    route = parse_message(message)
    route_function = SMS_ROUTES[route['route']]
    if from_number == MY_NUMBER and route_function:
        response = route_function(request, *route['args'])
    else:
        response = forward_message_to_me(from_number, message)

    if isinstance(response, dict):
        return sendsms(request, response)
    return HttpResponse("Complete.")

def forward_message_to_me(number, message):
    return {MY_NUMBER: "{}: {}".format(number, message)}


def sendsms(request, message_dict):
    if DEBUG:
        return HttpResponse('Debug')
    for number, message in message_dict.items():
        twilio_client.messages.create(
            body=message,
            to=number,
            from_=TWILIO_NUMBER)
    return HttpResponse('Sent.')
