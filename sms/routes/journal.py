""" journal deals with any routes that involve reading from, writing to,
    or doing operations on the journal app. """

from journal.models import Entry

def write_entry(name, number=None, *comments):
    """ Creates a journal entry. """

    comment = " ".join(comments)
    # We don't know whether the second parameter is a rating or comment in a
    # ratingless entry, so we test to be on the safe side
    try:
        number = int(number)
    except ValueError: # It was a comment after all
        comment = number + " " + comment
        number = None
    except TypeError: # It's a None
        pass

    comment = None if not comment else comment # explicit null vs empty string
    Entry.objects.create(name=name, rating=number, comment=comment)


def read_entry(name, from_latest=1):
    """ Reads the entry with {name}, {from_latest} most recent.

        from_latest is the human latest, not computer latest.
        ie 1 is most recent, 2 is second most recent, etc. """

    entry_list = Entry.objects.filter(name=name).order_by('-created_at')
    try:
        entry = entry_list[max(0, from_latest-1)]
        return str(entry)
    except IndexError:
        return ""

journal_routes = {"write": write_entry,
                  "read": read_entry,
                  }
