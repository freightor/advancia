from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from employers.models import Employee, WorkDetail
from transactions.models import Transaction

# Create your views here.


@api_view(["POST"])
def run_transaction(request):
    if request.method == "POST":
        employee_num = request.POST.get("employee_no")
        amount = Decimal(request.POST.get("amount"))
        order_id = request.POST.get("order_id")
        store = request.user.storeuser.store
        wk = get_object_or_404(WorkDetail, employee_no=employee_num)
        employee = wk.employee
        if employee and employee.active:
            if employee.monthly_advancia_limit - employee.monthly_advancia_total >= amount:
                Transaction.objects.create(
                    employee=employee,
                    amount=amount,
                    store=store,
                    order_id=order_id
                )
                data = {"message":"Transaction Succesful!"}
            else:
                data = {"message":"Failed! Monthly limit reached!"}
        else:
            data = {"message":"Failed! Not a valid Employee"}
        return Response(data=data)

@api_view(["GET"])
def tester(request):
    content = {
        "user": str(request.user),
        "store": str(request.user.storeuser.store)
    }
    return Response(content)