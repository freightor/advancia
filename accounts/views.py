from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ViewDoesNotExist
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import SignUpForm
from companies.models import Employee
# Create your views here.


def signup(request, user_type):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if user_type == "employer":
                Employee.objects.create(
                    user=user, role="admin", user_type="employee",created_by=user)
                return redirect("companies:new_employer")
            elif user_type == "merchant":
                Merchant.objects.create(
                    user=user, role="admin", user_type="merchant", created_by=user)
                # return redirect("shop:new_store")
                pass
            else:
                raise ViewDoesNotExist
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request,user)
                if hasattr(user,"merchant"):
                    pass
                    # return redirect("merchants:index")
                return redirect("companies:employee_list")
    else:
        form = AuthenticationForm()
        user = auth.get_user(request)
        if user.is_authenticated:
            if hasattr(user, "merchant"):
                pass
                # return redirect("shop:product_list")
            elif user.employee.role == "admin":
                return redirect("companies:employee_list")
            else:
                pass
                # return redirect("shop:shop_home")
    return render(request,"accounts/login.html",{"form":form})

def logout_view(request):
    logout(request)
    return redirect("accounts:login")