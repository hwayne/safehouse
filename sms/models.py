from django.db import models
from django import template


class Message(models.Model):
    phone_number = models.CharField(max_length=16)
    message = models.TextField()

    def __str__(self):
        return "{}: {}".format(self.phone_number, self.message)


def log_message(phone_number, message):
    Message(phone_number=phone_number, message=message).save()
    return message


class SavedMessage(models.Model):
    phone_number = models.CharField(max_length=16)
    message = models.TextField()
    tag = models.CharField(max_length=16)

    def __str__(self):
        return "{}: {}".format(self.tag, self.message)


def save_tagged_message(tag, phone_number, message):
    print(tag)
    print(phone_number)
    print(message)
    SavedMessage(tag=tag, phone_number=phone_number, message=message).save()


def pop_message_tag(tag):
    message = SavedMessage.objects.filter(tag=tag).first()
    if message:
        message.delete()
    return message



class Config(models.Model):
    """ Persistant server state beyond cache resets. """
    key = models.CharField(max_length=16, unique=True)
    val = models.CharField(max_length=16)

    def __str__(self):
        return "{}: {}".format(self.key, self.val)

def config(key, val):
    """ Sets and unsets server variables

    Takes in key, val. If val is Falsey, delete key if it exists."""
    if not val:
        [c.delete() for c in Config.objects.filter(key=key) ]
        return
    try:
        config = Config.objects.get(key=key)
        config.val = val
        config.save()
    except Config.DoesNotExist:
        Config(key=key, val=val).save()

class Template(models.Model):
    name = models.CharField(max_length=16, unique=True)
    text = models.TextField()

    def __str__(self):
        return "{}: {}".format(self.name, self.text)

    def as_template(self):
        return template.Template(self.text)



