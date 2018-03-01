from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from employers.models import Employee, Employer, WorkDetail, PaymentDetail
from employers.forms import AddressForm, EmployeeForm, EmployerForm, DepartmentForm

# Create your views here.


def dashboard(request):
    return render(request, "employers/dashboard.html")


def employee_list(request):
    employer = request.user.administrator.employer
    queryset = Employee.objects.filter(employer=employer)
    return render(request, "employers/employee_list.html", {"employees": queryset})


def new_employee(request):
    employer = request.user.administrator.employer
    if request.method == "POST":
        form = EmployeeForm(request.POST, prefix="employee")
        addr = AddressForm(request.POST, prefix="addr")
        if form.is_valid() and addr.is_valid():
            employee = form.save(commit=False)
            employee.created_by = request.user
            employee.employer = employer
            employee.address = addr.save()
            employee.save()
            return redirect("employers:employee_detail", pk=employee.pk)
    else:
        form = EmployeeForm(prefix="employee")
        addr = AddressForm(prefix="addr")
    return render(request, "employers/new_employee.html", {"form": form, "addr": addr})


def edit_employee(request, pk):
    employer = request.user.administrator.employer
    obj = get_object_or_404(Employee.objects.filter(employer=employer), pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=obj, prefix="employee")
        addr = AddressForm(request.POST, instance=obj.address, prefix="addr")
        if form.is_valid() and addr.is_valid():
            employee = form.save(commit=False)
            employee.edited_by = request.user
            addr.save()
            employee.save()
            return redirect("employers:employee_detail", pk=pk)
    else:
        form = EmployeeForm(instance=obj, prefix="employee")
        addr = AddressForm(instance=obj.address, prefix="addr")
    return render(request, "employers/new_employee.html", {"form": form, "addr": addr})


def employee_detail(request, pk):
    employer = request.user.administrator.employer
    employee = get_object_or_404(Employee.objects.filter(employer=employer))
    return render(request, "employers/employee_detail.html", {"employee": employee})


def activate_employee(request, pk):
    employer = request.user.administrator.employer
    employee = get_object_or_404(Employee.objects.filter(employer=employer))
    if employee.active:
        employee.active = False
    else:
        employee.active = True
    employee.save()
    return redirect("employers:employee_list")


def new_employer(request):
    if request.method == "POST":
        form = EmployerForm(request.POST, request.FILES, prefix="employer")
        addr = AddressForm(request.POST, prefix="addr")
        if form.is_valid() and addr.is_valid():
            employer = form.save(commit=False)
            employer.address = addr.save()
            employer.created_by = request.user
            employer.save()
            administrator = request.user.administrator
            administrator.employer = employer
            administrator.save()
            return redirect("employers:employee_list")
    else:
        form = EmployerForm(prefix="employer")
        addr = AddressForm(prefix="addr")
    return render(request, "employers/new_employer.html", {"form": form, "addr": addr})


def edit_employer(request):
    obj = request.user.administrator.employer
    if request.method == "POST":
        form = EmployerForm(request.POST, request.FILES,
                            instance=obj, prefix="employer")
        addr = AddressForm(request.POST, instance=obj.address, prefix="addr")
        if form.is_valid() and addr.is_valid():
            employer = form.save(commit=False)
            employer.edited_by = request.user
            employer.save()
            addr.save()
            return redirect("employers:employee_list")
    else:
        form = EmployerForm(prefix="employer", instance=obj)
        addr = AddressForm(prefix="addr", instance=obj.address)
    return render(request, "employers/new_employer.html", {"form": form, "addr": addr})


def new_department(request):
    employer = request.user.administrator.employer
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.created_by = request.user
            dept.employer = employer
            dept.save()
            return redirect("employers:dept_list")
    else:
        form = DepartmentForm()
    return render(request, "employers/dept_list.html", {"form": form})
