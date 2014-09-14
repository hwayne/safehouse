from django.db import models

# Create your models here.
class Entry(models.Model):
    class Meta:
        verbose_name_plural = "Entries"
    name = models.CharField(max_length=16)
    rating = models.IntegerField(null=True) # Maximum
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {} - {}".format(self.name, self.rating, self.comment)

