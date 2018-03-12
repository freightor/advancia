import time
from django.db import models
from binascii import unhexlify
from django.db import models
from django.conf import settings
from django_otp.models import Device
from django_otp.oath import TOTP
from django_otp.util import random_hex, hex_validator
from employers.models import Employee


class TOTPDevice(Device):
    """
    Manage generation and verification of OTP tokens for employees
    """
    key = models.CharField(max_length=40, default=random_hex(
        30), validators=[hex_validator], unique=True)
    last_verified_counter = models.BigIntegerField(default=-1)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    step = settings.TOTP_TOKEN_VALIDITY
    digits = settings.TOTP_DIGITS

    @property
    def bin_key(self):
        return unhexlify(self.key.encode())

    def totp_object(self):
        # Create TOTP object
        totp = TOTP(key=self.bin_key, step=self.step, digits=self.digits)

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
            if totp.verify(token, tolerance=tolerance):
                self.verified = True
                self.save()
        return self.verified
