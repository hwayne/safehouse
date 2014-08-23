from django.db import models


class ContactManager(models.Manager):

    def sample(self, count):
        """ Efficient random selection of contacts.

        We have this because randomly ordering the database is insanely slow.
        We use to ensure that when hitting the panic button, we don't know
        who it alerted, so we don't feel shunned if they don't respond.
        Does not get uninformed people.
        """

        from random import sample

        indices = list(self.all().values_list('id', flat=True))
        sampled_indices = sample(indices, min(int(count), len(indices)))
        return self.filter(id__in=sampled_indices, informed=True)

    def inform_all(self):
        """ Sets people as notified, returns list of who changed.

        Contacts start out as uninformed, aka they don't know about Safehouse.
        Since panicking at people would be weird, they never get 'normal'
        messages. Call inform_all to set them as "will get an informational
        text from safehouse." sms uses this to find who to text.
        """
        uninformed = self.filter(informed=False)
        for u in uninformed:
            u.informed = True
            u.save()
        return uninformed


class Contact(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    informed = models.BooleanField(default=False)
    objects = ContactManager()

    def __str__(self):
        return self.first_name + " " + \
            self.last_name + ": " + self.phone_number

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class Incident(models.Model):
    incident_date = models.DateTimeField('Time of Incident')
    contact_size = models.IntegerField()

    def __str__(self):
        return str(self.contact_size) + \
            " people contacted at " + \
            str(self.incident_date)
