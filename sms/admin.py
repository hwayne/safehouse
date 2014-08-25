from django.contrib import admin
from sms.models import Message, Template

admin.site.register(Message)
admin.site.register(Template)
