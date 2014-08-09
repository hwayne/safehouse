from django.db import models


class ContactManager(models.Manager):

    def sample(self, count):
        from random import sample

        indices = list(self.all().values_list('id', flat=True))
        sampled_indices = sample(indices, min(int(count), len(indices)))
        return self.filter(id__in=sampled_indices, informed=True)


class Contact(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    informed = models.BooleanField(default=False)
    objects = ContactManager()

    def __str__(self):
        return self.first_name + " " + \
            self.last_name + ": " + self.phone_number


class Incident(models.Model):
    incident_date = models.DateTimeField('Time of Incident')
    contact_size = models.IntegerField()

    def __str__(self):
        return str(self.contact_size) + \
            " people contacted at " + \
            str(self.incident_date)
