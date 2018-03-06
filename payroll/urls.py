from django.urls import path
from payroll import views

app_name = "payroll"
urlpatterns = [
    path("", views.payroll_list, name="payrolls"),
    path("generate/", views.generate_payrolls, name="gen_pay"),
    path("payslips/", views.generate_payslips, name="payslips")
]