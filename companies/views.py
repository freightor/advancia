from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from companies.models import Employee, Employer
from accounts.forms import ProfileForm
from companies.forms import AddressForm
from companies.forms import EmployerForm

# Create your views here.


def employee_list(request):
    employer = request.user.administrator.employer
    queryset = Employee.objects.filter(employer=employer)
    return render(request, "companies/employee_list.html", {"employees": queryset})


def new_employee(request):
    employer = request.user.administrator.employer
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            new_guy = Employee(user=user, employer=employer,
                               user_type="employee")
            new_guy.created_by = request.user
            new_guy.save()
            return redirect("companies:employee_detail")
    else:
        form = ProfileForm()
    return render(request, "companies/new_employee.html", {"form": form})


def edit_employee(request, pk):
    obj = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("companies:employee_detail", pk=pk)
    else:
        form = ProfileForm(instance=obj)
    return render(request, "companies/new_employee.html", {"form": form})


def new_employer(request):
    if request.method == "POST":
        form = EmployerForm(request.POST, request.FILES, prefix="employer")
        addr = AddressForm(request.POST, prefix="addr")
        if form.is_valid() and addr.is_valid():
            employer = form.save(commit=False)
            address = addr.save(commit=False)
            address.created_by = request.user
            address.save()
            employer.address = address
            employer.created_by = request.user
            employer.save()
            employee = request.user.employee
            employee.employer = employer
            employee.save()
            return redirect("companies:employee_list")
    else:
        form = EmployerForm(prefix="employer")
        addr = AddressForm(prefix="addr")
    return render(request, "companies/new_employer.html", {"form": form, "addr": addr})


def edit_employer(request):
    obj = request.user.employee.employer
    if request.method == "POST":
        form = EmployerForm(request.POST, request.FILES,
                            instance=obj, prefix="employer")
        addr = AddressForm(request.POST, instance=obj.address, prefix="addr")
        if form.is_valid() and addr.is_valid():
            employer = form.save(commit=False)
            address = addr.save(commit=False)
            address.edited_by = request.user
            address.save()
            employer.edited_by = request.user
            employer.save()
            return redirect("companies:employee_list")
    else:
        form = EmployerForm(prefix="employer")
        addr = AddressForm(prefix="addr")
    return render(request, "companies/new_company.html", {"form": form, "addr": addr})
