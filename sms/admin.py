from django.contrib import admin
from sms.models import Message, Template, Config, SavedMessage, DelayedCommand

admin.site.register(Message)
admin.site.register(SavedMessage)
admin.site.register(Template)
admin.site.register(Config)
admin.site.register(DelayedCommand)
