import datetime as dt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from payroll.models import Employee, Payroll
from common.decorators import admin_staff_required

# Create your views here.
@login_required
@admin_staff_required
def generate_payrolls(request):
    employer = request.user.administrator.employer
    for employee in Employee.objects.filter(employer=employer, active=True):
        Payroll.objects.create(employee=employee)
    return redirect("payroll:payrolls")


@login_required
def payroll_list(request):
    employer = request.user.administrator.employer
    payrolls = Payroll.objects.filter(employee__employer=employer)
    return render(request, "payroll/payrolls.html", {"payrolls": payrolls})


@login_required
def generate_payslips(request):
    return render(request, "payroll/payslips.html")
