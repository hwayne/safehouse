from django.db import models
from django.utils.timezone import now


class NotifierManager(models.Manager):
    def due_notifications(self):
        """ Gets all due notifications. Note it DOES NOT get notifications
        updated relatively soon, so as not to get swamped with notes every
        hour.

        NOTE: This means that modifying a notification in the admin database
        WILL reset the notification interval. Either consider it 'pinged'
        and act on it or use objects.filter.update to update it."""
        return (m for m in self.all() if m.can_notify()
                and (now() - m.updated_at).days >= m.notify_interval)


class Notifier(models.Model):
    """ Model that tracks how long it's been since certain types of entries
        were placed in a table. Used to send notifies to me when, say,
        I haven't added anything new to my 'gtd' saved messages,
        or haven't gone biking in a few days.

        model: Name of the model the notify watches.
               The model must have a Date or DateTime field.
        column: Name of the column we're watching for new entries.
                If null, will watch for any new entries in the model.
        column_val: The value we're watching for new entries.
                    For example, a tag we're tracking the use of.
                    null IFF column is null.
        notify_text: The text sent to you if it's been too long.
        notify_interval: How long to wait before reminding you.
        notifies_left: How many times this model should remind you.
                        If negative, will never "run out".
    """

    model = models.CharField(max_length=32)
    column = models.CharField(max_length=32, null=True)
    column_val = models.TextField(null=True)
    notify_text = models.TextField()
    notify_interval = models.IntegerField()
    notifies_left = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = NotifierManager()


    def __str__(self):
        return "\"{}\" | interval - {}, left - {}".format(self.notify_text,
                                                          self.notify_interval,
                                                          self.notifies_left)

    def get_model_class(self):
        """ Searches the project global for the django model who's name matches
            the 'model' column.

            returns the first model that matches. Undefined behavior if
            the model name is not unique. """
        model_list = [m for m in models.get_models()
                      if m.__name__.lower() == self.model.lower()]
        return model_list[0]

    def get_most_recent_model(self, order_method):
        """If column and column_val are defined, retrieve most recent row
           which has column_val in column.
           Otherwise, retrieve the most recently created row in the table."""
        model_class = self.get_model_class()
        filters = {self.column: self.column_val} if self.column else {}
        model = model_class.objects.filter(**filters).order_by('-'+order_method)
        return model[0]

    def can_notify(self):
        """ Returns whether or not a notify is due.
            Should be the only thing calling calling methods in this class. """

        date_method = get_date_method(self.get_model_class())
        most_recent = self.get_most_recent_model(date_method)
        time_since_last = now() - getattr(most_recent, date_method)
        if self.notifies_left != 0 \
                and time_since_last.days >= self.notify_interval:
            return True
        return False


def get_date_method(model_class):
    """Searches the model class for any datetime columns, and returns
       the name of the first it finds. If it can't find any, throw error."""
    for field in model_class._meta.fields:
        f = models.fields
        if isinstance(field, f.DateTimeField):
            return field.column
    raise AttributeError("No time or datetime fields")



class NotifierNumber(models.Model):
    """ Model that determines what numbers receive notifications. """

    notifier = models.ForeignKey(Notifier)
    phone_number = models.CharField(max_length=16)

    def __str__(self):
        return "{} | {}".format(self.phone_number, str(self.notifier))
