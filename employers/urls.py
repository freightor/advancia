from django.urls import path
from employers import views

app_name = "employers"
urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employer/add/", views.new_employer, name="new_employer")
]
