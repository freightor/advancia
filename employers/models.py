import os
import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from common.models import BaseModel, ActiveModel
from common.utils import make_employee_id
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


class Employer(BaseModel, ActiveModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    logo = models.ImageField(upload_to=logo_location, null=True, blank=True)
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    description = models.TextField()


class JobTitle(models.Model):
    name = models.CharField(max_length=255)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)


class Department(BaseModel, ActiveModel):
    name = models.CharField(max_length=200)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)


def admin_avatar_location(instance, filename):
    file_ext = os.path.splitext(filename)[1]
    return "logos/admins/employer_{0}{1}".format(instance.id, file_ext)


class Administrator(BaseModel, Profile):
    avatar = models.ImageField(
        null=True, blank=True, upload_to=admin_avatar_location)
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(max_length=10, default="employer")


class Employee(BaseModel, ActiveModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, null=True, blank=True)
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


class Payroll(BaseModel):
    date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    bonus = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    allowances = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    deductions = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)

    @property
    def employer(self):
        return self.employee.employer

    @property
    def month(self):
        return self.date.month

    @property
    def year(self):
        return self.date.year

    @property
    def name(self):
        return "{0}_{1}".format(self.month, self.year)

    @property
    def gross_salary(self):
        return self.basic_salary + self.bonus + self.allowances

    @property
    def ssf_employee(self):
        return Decimal(self.gross_salary * Decimal('0.05')).quantize(Decimal('.01'))

    @property
    def ssf_employer(self):
        return Decimal(self.gross_salary * Decimal('0.3')).quantize(Decimal('.01'))

    @property
    def taxable_income(self):
        return self.gross_salary - self.ssf_employee

    @property
    def paye(self):
        return Decimal(self.taxable_income * Decimal('0.14')).quantize(Decimal('.01'))

    @property
    def net_salary(self):
        return self.taxable_income - self.deductions

    def save(self, *args, **kwargs):
        self.basic_salary = self.employee.workdetail.basic_salary
        self.allowances = self.employee.paymentdetail.allowances
        self.bonus = self.employee.paymentdetail.bonus
        self.deductions = self.employee.paymentdetail.deductions
        super().save(*args, **kwargs)
