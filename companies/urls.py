from django.urls import path
from companies import views

app_name = "companies"
urlpatterns = [
    path("employees/", views.employee_list, name="employee_list"),
    path("employer/add/", views.new_employer, name="new_employer")
]
