import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel
from accounts.models import Profile

# Create your models here.

class Address(models.Model):
    location = models.CharField(max_length=255)
    postal_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "addresses"


def logo_location(instance, filename):
    file_ext = os.path.splitext(filename)[1]
    return "logos/employers/employer_{0}{1}".format(instance.id, file_ext)


class Employer(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    logo = models.ImageField(upload_to=logo_location, null=True, blank=True)
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    description = models.TextField()


class Employee(BaseModel, Profile):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salary = models.FloatField(null=True, blank=True)
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, null=True, blank=True)
    employee_no = models.CharField(
        max_length=30, unique=True, null=True, blank=True)
