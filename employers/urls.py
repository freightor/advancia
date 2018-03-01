from django.urls import path
from employers import views

app_name = "employers"
urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path("add/", views.new_employer, name="new_employer"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/<uuid:pk>/", views.employee_detail, name="employee_detail"),
    path("employees/add", views.new_employee, name="new_employee"),
    path("employees/<uuid:pk>/edit", views.edit_employee, name="edit_employee"),
]
