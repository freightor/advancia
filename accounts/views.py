from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ViewDoesNotExist
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import SignUpForm
from employers.models import Administrator
from stores.models import StoreUser
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
                Administrator.objects.create(user=user, role="admin",created_by=user)
                return redirect("employers:new_employer")
            elif user_type == "store":
                StoreUser.objects.create(user=user, role="admin",created_by=user)
                return redirect("stores:new_store")
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
                if hasattr(user,"storeuser"):
                    return redirect("stores:dashboard")
                return redirect("employers:dashboard")
    else:
        form = AuthenticationForm()
        user = auth.get_user(request)
        if user.is_authenticated:
            if hasattr(user, "storeuser"):
                return redirect("stores:dashboard")
            elif hasattr(user, "administrator"):
                return redirect("employers:dashboard")
            else:
                raise ViewDoesNotExist
    return render(request,"accounts/login.html",{"form":form})

def logout_view(request):
    logout(request)
    return redirect("accounts:login")