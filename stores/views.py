from django.shortcuts import render, get_object_or_404, redirect
from transactions.models import Transaction
from stores.forms import StoreForm
from employers.forms import AddressForm
from rest_framework.authtoken.models import Token
from common.decorators import admin_storeuser_required
from django.contrib.auth.decorators import login_required

# Create your views here.\
@login_required
@admin_storeuser_required
def dashboard(request):
    store = request.user.storeuser.store
    return render(request,"stores/dashboard.html",{"store":store})

@login_required
@admin_storeuser_required
def transaction_list(request):
    store = request.user.storeuser.store
    queryset = Transaction.objects.filter(store=store)
    return render(request, "stores/transaction_list.html", {"transactions": queryset})

@login_required
@admin_storeuser_required
def transaction_detail(request, pk):
    store = request.user.storeuser.store
    transaction = get_object_or_404(
        Transaction.objects.filter(store=store), pk=pk)
    return render(request, "stores/transaction_detail.html", {"transaction": transaction})

@login_required
@admin_storeuser_required
def new_store(request):
    if request.method == "POST":
        form = StoreForm(request.POST, prefix="form")
        addr = AddressForm(request.POST, prefix="addr")
        if form.is_valid() and addr.is_valid():
            store = form.save(commit=False)
            store.created_by = request.user
            store.address = addr.save()
            store.save()
            store_user = request.user.storeuser
            store_user.store = store
            store_user.save()
            return redirect("stores:dashboard")
    else:
        form = StoreForm(prefix="form")
        addr = AddressForm(prefix="addr")
    return render(request, "stores/new_store.html", {"form": form, "addr": addr})
