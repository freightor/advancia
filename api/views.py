from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from employers.models import Employee, WorkDetail
from transactions.models import Transaction
from common.utils import send_sms
from otp.models import TOTPDevice

# Create your views here.


@api_view(["POST"])
def run_transaction(request):
    if request.method == "POST":
        employee_num = request.POST.get("employee_no")
        wk = get_object_or_404(WorkDetail, employee_no=employee_num)
        if wk.employee:
            request.session["employee"] = wk.employee.id
            s_code = TOTPDevice.objects.create(user=wk.employee).generate_token()
            send_sms("+2330201415087",s_code)
            data = {"message":"Verification sent!"}
        else:
            data = {"message": "Failed! Not a valid Employee"}
        return Response(data=data)


@api_view(["POST"])
def verify_transaction(request):
    if request.method == "POST":
        token = request.POST.get("token")
        amount = Decimal(request.POST.get("amount"))
        order_id = request.POST.get("order_id")
        store = request.user.storeuser.store
        employee = get_object_or_404(Employee, pk=int(request.session.get("employee")))
        last_token = employee.totpdevice_set.last()
        if last_token.verify_token(token):
            if employee.monthly_advancia_limit - employee.monthly_advancia_total >= amount:
                Transaction.objects.create(
                    employee=employee,
                    amount=amount,
                    store=store,
                    order_id=order_id
                )
                request.session.pop("employee")
                data = {"message": "Transaction Succesful!"}
            else:
                data = {"message":"Failed! Monthly limit reached!"}
        else:
            data = {"message": "Wrong Code, Try Again!"}
        return Response(data=data)
