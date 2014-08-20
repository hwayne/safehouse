from django.views import generic
from django.http import HttpResponse
from panic.models import Contact


class DetailView(generic.DetailView):
    model = Contact


def index(request):
    return HttpResponse("panic place.")
