import string
import random
import uuid
import time
from django_otp.oath import TOTP
from django_otp.util import random_hex
from twilio.rest import Client
from django.conf import settings


def make_employee_id(instance):
    Klass = instance.__class__
    new_code = "".join(random.sample(string.ascii_uppercase,
                                     3)+random.sample(string.digits, 3))
    if Klass.objects.filter(employee_no=new_code).exists():
        return make_employee_id(instance)
    return new_code


def make_ref():
    return uuid.uuid1().hex.upper()


def send_sms(to_number, token):
    # Send Verification code using Twilio
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_NUMBER
    client = Client(account_sid, auth_token)
    client.api.messages.create(
        to=to_number, from_=twilio_number, body="Your Advancia OTP is: {0}".format(str(token)))


def send_test_sms(token):
    # Send Verification code using Twilio
    account_sid = settings.TWILIO_TEST_ACCOUNT_SID
    auth_token = settings.TWILIO_TEST_AUTH_TOKEN
    twilio_number = settings.TWILIO_TEST_FROM
    client = Client(account_sid, auth_token)
    client.api.messages.create(
        to=settings.TWILIO_TEST_TO, from_=twilio_number, body="Your Advancia OTP is: {0}".format(str(token)))