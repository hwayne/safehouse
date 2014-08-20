from django.db import models


class Message(models.Model):
    phone_number = models.CharField(max_length=16)
    message = models.TextField()

    def __str__(self):
        return "{}: {}".format(self.phone_number, self.message)


def log_message(phone_number, message):
    Message(phone_number=phone_number, message=message).save()
    return message
