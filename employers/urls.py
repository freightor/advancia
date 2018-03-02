from django.urls import path
from employers import views

app_name = "employers"
urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path("add/", views.new_employer, name="new_employer"),
    path("admins/", views.admin_list, name="admins"),
    path("admins/add/", views.new_admin, name="new_admin"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/<uuid:pk>/", views.employee_detail, name="employee_detail"),
    path("employees/add/", views.new_employee, name="new_employee"),
    path("employees/<uuid:pk>/edit/", views.edit_employee, name="edit_employee"),
    path("employees/<uuid:pk>/details/edit/", views.edit_details, name="edit_details"),
    path("employees/<uuid:pk>/activate/", views.activate_employee, name="activate_employee"),
    path("payrolls/", views.payroll_list, name="payrolls"),
    path("payrolls/generate/", views.generate_payrolls, name="gen_pay"),
    path("payslips/", views.generate_payslips, name="payslips")
]
