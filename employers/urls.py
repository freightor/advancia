from django.urls import path
from employers import views

app_name = "employers"
urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path("add/", views.new_employer, name="new_employer"),
    path("admins/", views.admin_list, name="admins"),
    path("admins/<int:pk>/", views.admin_profile, name="admin_profile"),
    path("admins/<int:pk>/edit/", views.edit_admin, name="edit_admin"),
    path("settings/", views.edit_employer,name="settings"),
    path("departments/", views.dept_list,name="dept_list"),
    path("departments/add", views.new_department,name="new_dept"),
    path("departments/<int:pk>/edit", views.edit_department,name="edit_dept"),
    path("departments/<int:pk>/delete", views.delete_dept,name="delete_dept"),
    path("admins/add/", views.new_admin, name="new_admin"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/<int:pk>/", views.employee_detail, name="employee_detail"),
    path("employees/add/", views.new_employee, name="new_employee"),
    path("employees/<int:pk>/edit/", views.edit_employee, name="edit_employee"),
    path("employees/<int:pk>/details/edit/", views.edit_details, name="edit_details"),
    path("employees/<int:pk>/activate/", views.activate_employee, name="activate_employee"),
    path("employees/upload/", views.upload_users, name="upload")
]
