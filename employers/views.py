import datetime as dt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import SignUpForm
from employers.models import Employee, Employer, WorkDetail, PaymentDetail,Administrator, Department
from employers.forms import AddressForm, EmployeeForm, EmployerForm, DepartmentForm, WorkDetailForm, PaymentDetailForm, AdministratorForm, FileUploadForm
from common.decorators import admin_staff_required

# Create your views here.


@login_required
def dashboard(request):
    employer = request.user.administrator.employer
    return render(request, "employers/dashboard.html",{"employer":employer})


@login_required
def admin_list(request):
    employer = request.user.administrator.employer
    admins = Administrator.objects.filter(employer=employer)
    return render(request, "employers/users.html", {"admins": admins})


@login_required
def employee_list(request):
    employer = request.user.administrator.employer
    queryset = Employee.objects.filter(employer=employer)
    return render(request, "employers/employee_list.html", {"employees": queryset})


@login_required
@admin_staff_required
def new_employee(request):
    employer = request.user.administrator.employer
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, prefix="employee")
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


@login_required
def edit_employee(request, pk):
    employer = request.user.administrator.employer
    obj = get_object_or_404(Employee.objects.filter(employer=employer), pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES,
                            instance=obj, prefix="employee")
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


@login_required
def employee_detail(request, pk):
    employer = request.user.administrator.employer
    employee = get_object_or_404(
        Employee.objects.filter(employer=employer), pk=pk)
    return render(request, "employers/employee_detail.html", {"employee": employee})


@login_required
@admin_staff_required
def activate_employee(request, pk):
    employer = request.user.administrator.employer
    employee = get_object_or_404(
        Employee.objects.filter(employer=employer), pk=pk)
    if employee.active:
        employee.active = False
    else:
        employee.active = True
    employee.save()
    return redirect("employers:employee_list")


@login_required
@admin_staff_required
def edit_details(request, pk):
    employer = request.user.administrator.employer
    employee = get_object_or_404(
        Employee.objects.filter(employer=employer), pk=pk)
    if request.method == "POST":
        work = WorkDetailForm(employer, request.POST,
                              instance=employee.workdetail, prefix="work")
        payment = PaymentDetailForm(
            request.POST, instance=employee.paymentdetail, prefix="pay")
        if work.is_valid() and payment.is_valid():
            work.save()
            payment.save()
            return redirect("employers:employee_detail", pk=employee.pk)
    else:
        work = WorkDetailForm(
            employer, instance=employee.workdetail, prefix="work")
        payment = PaymentDetailForm(
            instance=employee.paymentdetail, prefix="pay")
    return render(request, "employers/edit_details.html", {"work": work, "payment": payment})


@login_required
@admin_staff_required
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
            return redirect("employers:new_dept")
    else:
        form = EmployerForm(prefix="employer")
        addr = AddressForm(prefix="addr")
    return render(request, "employers/new_employer.html", {"form": form, "addr": addr})


@login_required
@admin_staff_required
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
            return redirect("employers:dashboard")
    else:
        form = EmployerForm(prefix="employer", instance=obj)
        addr = AddressForm(prefix="addr", instance=obj.address)
    return render(request, "employers/settings.html", {"form": form, "addr": addr})


@login_required
@admin_staff_required
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
    return render(request, "employers/new_dept.html", {"form": form})


@login_required
@admin_staff_required
def edit_department(request, pk):
    employer = request.user.administrator.employer
    obj = get_object_or_404(
        Department.objects.filter(employer=employer), pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=obj)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.edited_by = request.user
            dept.save()
            return redirect("employers:dept_list")
    else:
        form = DepartmentForm(instance=obj)
    return render(request, "employers/new_dept.html", {"form": form})


@login_required
def dept_list(request):
    employer = request.user.administrator.employer
    queryset = Department.objects.filter(employer=employer)
    return render(request, "employers/dept_list.html", {"departments": queryset})


@login_required
@admin_staff_required
def delete_dept(request, pk):
    employer = request.user.administrator.employer
    obj = get_object_or_404(
        Department.objects.filter(employer=employer), pk=pk)
    obj.delete()
    return redirect("employers:dept_list")


@login_required
@admin_staff_required
def new_admin(request):
    employer = request.user.administrator.employer
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Administrator.objects.create(
                user=user, employer=employer, role="regular", created_by=request.user)
            return redirect("employers:admins")
    else:
        form = SignUpForm()
    return render(request, "employers/new_admin.html", {"form": form})

@login_required
@admin_staff_required
def edit_admin(request,pk):
    employer = request.user.administrator.employer
    obj = get_object_or_404(Administrator.objects.filter(employer=employer),pk=pk)
    if request.method == "POST":
        form = SignUpForm(request.POST, instance=obj.user,prefix="form")
        admin = AdministratorForm(request.POST,request.FILES,instance=obj,prefix="admin")
        if form.is_valid() and admin.is_valid():
            admin.save(commit=False)
            admin.edited_by = request.user
            form.save()    
            return redirect("employers:admins")
    else:
        form = SignUpForm(instance=obj.user,prefix="form")
        admin = AdministratorForm(instance=obj,prefix="admin")
    return render(request, "employers/new_admin.html", {"form": form,"admin":admin})

@login_required
def admin_profile(request,pk):
    employer = request.user.administrator.employer
    admin = get_object_or_404(Administrator.objects.filter(employer=employer),pk=pk)
    return render(request,"employers/profile.html",{"admin":admin})

@login_required
@admin_staff_required
def upload_users(request):
    pass