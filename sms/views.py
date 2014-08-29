# from django.shortcuts import render
from sms.utils import parse_message, clean_number
from django.http import HttpResponse
from django.views import generic
from sms.models import log_message, Template
from sms.routes import ROUTES
from django_twilio.decorators import twilio_view
from sms.env import MY_NUMBER, TWILIO_NUMBER
from django_twilio.client import twilio_client


class TemplateView(generic.ListView):
    model = Template


@twilio_view
def index(request):
    from_number = clean_number(request.POST.get('From', '0'))
    message = request.POST.get('Body', '')
    log_message(from_number, message)  # for posterity!

    route = parse_message(message)
    route_function = ROUTES[route['route']]
    if from_number != MY_NUMBER:
        response = route_function(*route['args'])
    else:
        response = ROUTES['outside'](from_number, message)
    if isinstance(response, dict):
        return sendsms(request, response)
    return HttpResponse("Complete.")


def sendsms(request, message_dict):  # Reason it needs a response?
    for number, message in message_dict.items():
        twilio_client.messages.create(
            body=message,
            to=number,
            from_=TWILIO_NUMBER)
    return HttpResponse('Sent.')
