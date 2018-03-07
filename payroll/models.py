import os
from decimal import Decimal
from django.db import models
from employers.models import Employee
from common.models import BaseModel
from common.gra import get_tax
from django.conf import settings

# Create your models here.


class Payroll(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    bonus = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    allowances = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2)
    deductions = models.DecimalField(
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

    @property
    def employer(self):
        return self.employee.employer

    @property
    def month(self):
        return self.created_at.month

    @property
    def year(self):
        return self.created_at.year

    @property
    def name(self):
        return "{0}_{1}".format(self.month, self.year)

    def save(self, *args, **kwargs):
        self.basic_salary = self.employee.workdetail.basic_salary
        self.allowances = self.employee.paymentdetail.allowances
        self.bonus = self.employee.paymentdetail.bonus
        self.deductions = self.employee.paymentdetail.deductions
        self.gross_salary = self.basic_salary + self.bonus + self.allowances
        self.ssf_employee = self.gross_salary * settings.SSF_EMPLOYEE_RATE
        self.ssf_employer = self.gross_salary * settings.SSF_EMPLOYER_RATE
        self.taxable_income = self.gross_salary - self.ssf_employee
        self.paye = get_tax(self.taxable_income)
        self.net_salary = self.taxable_income - self.deductions
        super().save(*args, **kwargs)
