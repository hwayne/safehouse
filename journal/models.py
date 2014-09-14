from django.db import models

# Create your models here.


class Entry(models.Model):
    """ A journal entry, with the ability to rate it. Note that name is not
        unique, and is more a tag than an artistic style. Don't call an entry
        "A walk in the park" or "Very bad day", but 'park' or 'sad'. This
        Makes it much easier to integrate with the reminder app and to
        group entries by mood or type. """

    class Meta:
        verbose_name_plural = "Entries"
    name = models.CharField(max_length=16)
    rating = models.IntegerField(null=True)  # Maximum
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {} - {}".format(self.name, self.rating, self.comment)
