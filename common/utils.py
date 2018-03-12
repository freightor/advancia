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


class TransactionOTP:
    """
    A class to manage generation and verification of OTP tokens for employees
    """

    def __init__(self):

        # generate random secret key to use for token generation
        self.key = random_hex(30)
        self.verified = False
        self.number_of_digits = 6

        # Validity period for tokens in seconds
        self.token_validity_period = 60

    def totp_object(self):
        # Create TOTP object
        totp = TOTP(key=self.key, step=self.token_validity_period,
                    digits=self.number_of_digits)

        # Set TOTP time as current time
        totp.time = time.time()
        return totp

    def generate_token(self):
        #  Get TOTP object and use it to create a token
        totp = self.totp_object()
        # Get token from the totp object using totp.token() and convert to string
        token = str(totp.token()).zfill(6)
        return token

    def verify_token(self, token, tolerance=0):
        # convert token to integer
        try:
            token = int(token)
        except ValueError:
            # Return False if token cannot be converted to integer
            self.verified = False
        else:
            totp = self.totp_object()
            self.verified = totp.verify(token, tolerance=tolerance)


def send_sms(to_number, obj):
    # Send Verification code using Twilio
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_NUMBER
    client = Client(account_sid, auth_token)
    token = obj.totp_object().token()
    client.api.messages.create(
        to=to_number, from_=twilio_number, body="Your Advancia OTP is: {0}".format(str(token)))


def send_test_sms(obj):
    # Send Verification code using Twilio
    account_sid = settings.TWILIO_TEST_ACCOUNT_SID
    auth_token = settings.TWILIO_TEST_AUTH_TOKEN
    twilio_number = settings.TWILIO_TEST_FROM
    client = Client(account_sid, auth_token)
    token = obj.totp_object().token()
    client.api.messages.create(
        to=settings.TWILIO_TEST_TO, from_=twilio_number, body="Your Advancia OTP is: {0}".format(str(token)))