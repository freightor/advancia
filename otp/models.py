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
    key = models.CharField(max_length=60, default=random_hex(
        20), validators=[hex_validator], unique=True)
    last_verified_counter = models.BigIntegerField(default=-1)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    step = settings.TOTP_TOKEN_VALIDITY
    digits = settings.TOTP_TOKEN_DIGITS

    @property
    def bin_key(self):
        if isinstance(self.key, str):
            return unhexlify(self.key[2:-1].encode())
        return unhexlify(self.key)

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

    def verify_token(self, token):
        totp = self.totp_object()
        if not self.verified and totp.t() > self.last_verified_counter and totp.verify(token, tolerance=0):
            self.last_verified_counter = totp.t()
            self.verified = True
            self.save()
            return True
        return False
