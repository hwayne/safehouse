from django.db import models

# Create your models here.
class Entry(models.Model):
    tag = models.CharField(max_length=16)
    rating = models.IntegerField(null=True) # Maximum
    comment = models.TextField(null=True)

    def __str__(self):
        return "{} - {} - {}".format(

