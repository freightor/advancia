from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from employers.models import Employee, WorkDetail
from transactions.models import Transaction
from common.utils import send_test_sms, TransactionOTP

# Create your views here.


@api_view(["POST"])
def run_transaction(request):
    if request.method == "POST":
        employee_num = request.POST.get("employee_no")
        amount = Decimal(request.POST.get("amount"))
        order_id = request.POST.get("order_id")
        wk = get_object_or_404(WorkDetail, employee_no=employee_num)
        employee = wk.employee
        if employee and employee.active:
            if employee.monthly_advancia_limit - employee.monthly_advancia_total >= amount:
                request.session["employee"] = employee_num
                request.session["amount"] = amount
                request.session["order_id"] = order_id
                trans_otp = request.session.get("trans_otp", TransactionOTP())
                send_test_sms(trans_otp)
                data = {"message":"Verification sent!"}
            else:
                data = {"message": "Failed! Monthly limit reached!"}
        else:
            data = {"message": "Failed! Not a valid Employee"}
        return Response(data=data)


@api_view(["POST"])
def verify_transaction(request):
    if request.method == "POST":
        store = request.user.storeuser.store
        emp = get_object_or_404(Employee, employee_no=request.session["employee"])
        token = request.POST.get("otp_code")
        trans_otp = request.session.get("trans_otp")
        if trans_otp and trans_otp.verify_transaction(token):
            Transaction.objects.create(
                employee=emp,
                amount=request.session.get("amount"),
                store=store,
                order_id=request.session.get("order_id")
            )
            data = {"message": "Transaction Succesful!"}
        else:
            data = {"message": "Wrong Code, Try Again!"}
        return Response(data=data)
