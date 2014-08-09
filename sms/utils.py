import shlex
from re import sub
from sms.models import Message


def log_message(phone_number, message):
    Message(phone_number=phone_number, message=message).save()
    return message


def clean_number(number):
    return sub("\D", "", number)


def parse_message(message):
    """Breaks an input message (sms, email, etc) into a dict of form
       {'route': first_token, 'args': [array_of_rest_of_tokens]}"""
    message = "Empty Message" if not message else message
    token_list = shlex.split(message)
    route = token_list.pop(0).lower()
    return {'route': route, 'args': token_list}
