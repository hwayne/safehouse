from os import environ
from safehouse.settings import DEBUG  # Used in the sms view

MY_NUMBER = environ['MY_NUMBER']
MY_NAME = environ['MY_NAME']  # To Depreciate
TWILIO_NUMBER = environ['TWILIO_NUMBER']
