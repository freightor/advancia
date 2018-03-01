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


class Department(BaseModel):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Employer, on_delete=models.CASCADE)


class Administrator(BaseModel, Profile):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, default="employer")


class Employee(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
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
    marital_status = models.CharField(max_length=10,choices=MARITAL_STATUS_CHOICES, null=True,blank=True)


class WorkDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, null=True, blank=True)
    employee_no = models.CharField(
        max_length=30, unique=True, null=True, blank=True)
    date_of_employment = models.DateField()
    social_security_no = models.CharField(max_length=50, unique=True)


class PaymentDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    bonus = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    allowances = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    deductions = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    bonus = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    allowances = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    gross_salary = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    ssf_employee = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    ssf_employer = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    taxable_income = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    paye = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    net_salary = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
