import shlex
from re import sub
from sms.models import Message, Template
from sms.env import MY_NAME, MY_NUMBER
from django.template import Context, loader
from django.template.base import TemplateDoesNotExist



def clean_number(number):
    return sub("\D", "", number)


def parse_message(message):
    """Breaks an input message (sms, email, etc) into a dict of form
       {'route': first_token, 'args': [array_of_rest_of_tokens]}"""
    message = "Empty Message" if not message else message
    token_list = shlex.split(message)
    route = token_list.pop(0).lower()
    return {'route': route, 'args': token_list}


def get_templater(template_name='inform'):
    """ Get a template renderer for the route dicts.

        Will first look for core templates (in template folder), then
        will look for extension templates (in the Template model).

        Returns a function that, given a contact, renders the template. """
    template_url = template_name
    if 'html' not in template_url:  # Legacy
        template_url = "sms/{}.html".format(template_name)

    try:
        template = loader.get_template(template_url)
    except TemplateDoesNotExist:
        template = Template.objects.get(name=template_name).as_template()


    def context_maker(contact):
        return Context({'name': contact.first_name,
                        'my_number': MY_NUMBER,
                        'my_name': MY_NAME})

    def templater(contact):
        return template.render(context_maker(contact))

    return templater
