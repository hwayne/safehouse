from django.db import models
from datetime import date


class Reminder(models.Model):
    """ Model that tracks how long it's been since certain types of entries
        were placed in a table. Used to send reminders to me when, say,
        I haven't added anything new to my 'gtd' saved messages,
        or haven't gone biking in a few days.

        model: Name of the model the reminder watches.
               The model must have a Date or DateTime field.
        column: Name of the column we're watching for new entries.
                If null, will watch for any new entries in the model.
        column_val: The value we're watching for new entries.
                    For example, a tag we're tracking the use of.
                    null IFF column is null.
        reminder_text: The text sent to you if it's been too long.
        reminder_interval: How long to wait before reminding you.
        reminders_left: How many times this model should remind you.
                        If negative, will never "run out".
    """

    model = models.CharField(max_length=32)
    column = models.CharField(max_length=32, null=True)
    column_val = models.TextField(null=True)
    reminder_text = models.TextField()
    reminder_interval = models.IntegerField()
    reminders_left = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return reminder_text

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

    def can_remind(self):
        """ Returns whether or not a reminder is due.
            Should be the only thing calling calling methods in this class. """

        date_method = get_date_method(self.get_model_class())
        most_recent = self.get_most_recent_model(date_method)
        time_since_last = get_date(most_recent, date_method) - date.today()
        if self.reminders_left != 0 \
                and time_since_last.days >= self.reminder_interval:
            return True
        return False


# Add get time on model class, maybe? Optimization.

def get_date_method(model_class):
    """Searches the model class for any datetime or date columns, and returns
       the name of the first it finds. If it can't find any, throw error."""
    for field in model_class._meta.fields:
        f = models.fields
        if type(field) in (f.DateField, f.DateTimeField):
            return field.column
    raise AttributeError("No time or datetime fields")

def get_date(model, field_name):
    """ If field is a datefield, return it's value for the model.
        If the field is a datetime, return just the date.
        Otherwise, crash. """
    date_object = getattr(model, field_name)
    if type(date_object) == date:
        return date_object
    return date_object.date()

