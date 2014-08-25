from django.db import models


class Message(models.Model):
    phone_number = models.CharField(max_length=16)
    message = models.TextField()

    def __str__(self):
        return "{}: {}".format(self.phone_number, self.message)


class TemplateManager(models.Manager):

    def get_as_template(self, name):
        """ Get template from model, return as django template. """

        from django import template

        return template.Template(self.get(name=name).text)

class Template(models.Model):
    name = models.CharField(max_length=16, unique=True)
    text = models.TextField()
    objects = TemplateManager()

    def __str__(self):
        return "{}: {}".format(self.name, self.text)

def log_message(phone_number, message):
    Message(phone_number=phone_number, message=message).save()
    return message
