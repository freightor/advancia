from django.shortcuts import render, get_object_or_404, redirect
from transactions.models import Transaction

# Create your views here.


def transaction_list(request):
    store = request.user.storeuser.store
    queryset = Transaction.objects.filter(store=store)
    return render(request, "stores/transaction_list.html", {"transactions": queryset})


def transaction_detail(request, pk):
    store = request.user.storeuser.store
    transaction = get_object_or_404(Transaction.objects.filter(store=store), pk=pk)
    return render(request, "stores/transaction_detail.html", {"transaction": transaction})