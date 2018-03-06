import os
from decimal import Decimal
from django.db import models
from employers.models import Employee
from common.models import BaseModel
from common.gra import get_tax
from django.conf import settings

# Create your models here.


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
        return Decimal(self.gross_salary * settings.SSF_EMPLOYEE_RATE).quantize(settings.ONE_CENT)

    @property
    def ssf_employer(self):
        return Decimal(self.gross_salary * settings.SSF_EMPLOYER_RATE).quantize(settings.ONE_CENT)

    @property
    def taxable_income(self):
        return self.gross_salary - self.ssf_employee

    @property
    def paye(self):
        return get_tax(self.taxable_income)

    @property
    def net_salary(self):
        return self.taxable_income - self.deductions

    def save(self, *args, **kwargs):
        self.basic_salary = self.employee.workdetail.basic_salary
        self.allowances = self.employee.paymentdetail.allowances
        self.bonus = self.employee.paymentdetail.bonus
        self.deductions = self.employee.paymentdetail.deductions
        super().save(*args, **kwargs)
