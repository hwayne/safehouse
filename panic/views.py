from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http import HttpResponse
from panic.models import Contact
from panic.env import MY_NUMBER
from panic.view_utils import get_templater

DEFAULT_PANIC_NUMBER = MY_NUMBER  # config value
DEFAULT_PANIC_COUNT = 3


class DetailView(generic.DetailView):
    model = Contact


def index(request):
    return HttpResponse("panic place.")


def contact(request, name):
    contact_list = Contact.objects.filter(first_name=name)
    context = {
        'contact_list': contact_list,
        'name': name,
    }
    return render(request, 'panic/contacts.html', context)


def test(request):
    response = index(request)
    return HttpResponse(response.content + "asdasds")


def random(request, count=DEFAULT_PANIC_COUNT):
    contact_list = Contact.objects.sample(count)

    templater = get_templater('sms/panic.html')
    return response_from_type(request, contact_list, templater)

def inform(request):
    contact_list = Contact.objects.inform_all()
    if not contact_list:
        return HttpResponse("No Uninformed")

    templater = get_templater('sms/message.html')
    return response_from_type(request, contact_list, templater)

@csrf_exempt # internally called only
def response_from_type(request, contacts, templater):
    request_type = request.META.get('CONTENT_TYPE', 'html')

    # Used by an SMS or email route
    if 'internal' in request_type:
        return {contact.phone_number: templater(contact)
                for contact in contacts}

    # html requests should be for testing only.
    elif 'html' in request_type or 'text' in request_type:
        return HttpResponse(templater(contacts[0]))
