# File is implicitly tested by test_views.py

from django.template import Context, loader
from panic.env import MY_NUMBER, MY_NAME


def get_templater(template_url='panic/message.html'):
    context_maker = lambda contact: Context({'name': contact.first_name,
                                             'my_number': MY_NUMBER,
                                             'my_name': MY_NAME})

    template = loader.get_template(template_url)

    def templater(contact):
        return template.render(context_maker(contact))

    return templater
