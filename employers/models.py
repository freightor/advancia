import os
import uuid
from decimal import Decimal
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from common.models import BaseModel, ActiveModel
from common.utils import make_employee_id
from accounts.models import Profile
from common.gra import get_tax

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


class Employer(BaseModel, ActiveModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    logo = models.ImageField(upload_to=logo_location, null=True, blank=True)
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)


class JobTitle(models.Model):
    name = models.CharField(max_length=255)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)


class Department(BaseModel, ActiveModel):
    name = models.CharField(max_length=200)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)


def admin_avatar_location(instance, filename):
    file_ext = os.path.splitext(filename)[1]
    return "employer_{0}/admins/{1}{2}".format(instance.employer.id, instance.id, file_ext)


class Administrator(BaseModel, Profile):
    avatar = models.ImageField(
        null=True, blank=True, upload_to=admin_avatar_location)
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(max_length=10, default="employer")


def headshot_location(instance, filename):
    file_ext = os.path.splitext(filename)[1]
    return "employer_{0}/employees/{1}{2}".format(instance.employer.id, instance.id, file_ext)


class Employee(BaseModel, ActiveModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField()
    headshot = models.ImageField(upload_to=headshot_location, null=True, blank=True)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other")
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    MARITAL_STATUS_CHOICES = (
        ("married", "Married"),
        ("single", "Single"),
        ("engaged", "Engaged"),
        ("divorced", "Divorced")
    )
    marital_status = models.CharField(
        max_length=10, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def name(self):
        if self.middle_name:
            return "{0} {1} {2}".format(self.first_name, self.middle_name, self.last_name)
        return "{0} {1}".format(self.first_name, self.last_name)


class WorkDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(
        JobTitle, on_delete=models.SET_NULL, null=True, blank=True)
    basic_salary = models.DecimalField(
        default=0, max_digits=12, decimal_places=2)
    employee_no = models.CharField(
        max_length=30, unique=True, null=True, blank=True)
    date_of_employment = models.DateField(null=True, blank=True)
    social_security_no = models.CharField(
        max_length=50, unique=True, null=True, blank=True)


class PaymentDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    bonus = models.DecimalField(
        default=0, max_digits=12, decimal_places=2)
    allowances = models.DecimalField(
        default=0, max_digits=12, decimal_places=2)
    deductions = models.DecimalField(
        default=0, max_digits=12, decimal_places=2)


@receiver(post_save, sender=Employee)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        new_work = WorkDetail.objects.create(employee=instance)
        new_work.employee_no = make_employee_id(new_work)
        PaymentDetail.objects.create(employee=instance)
    instance.workdetail.save()
    instance.paymentdetail.save()