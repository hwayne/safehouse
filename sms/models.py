from django.db import models
from django import template


class Message(models.Model):
    phone_number = models.CharField(max_length=16)
    message = models.TextField()

    def __str__(self):
        return "{}: {}".format(self.phone_number, self.message)


class Template(models.Model):
    name = models.CharField(max_length=16, unique=True)
    text = models.TextField()

    def __str__(self):
        return "{}: {}".format(self.name, self.text)

    def as_template(self):
        return template.Template(self.text)


def log_message(phone_number, message):
    Message(phone_number=phone_number, message=message).save()
    return message
