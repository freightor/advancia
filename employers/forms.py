from django import forms
from employers.models import Employee, Employer, Address, WorkDetail, PaymentDetail, Department, Administrator


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("location", "postal_address", "phone", "email")

class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ("avatar","role")

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("first_name", "middle_name", "last_name",
                  "date_of_birth", "gender", "marital_status")


class WorkDetailForm(forms.ModelForm):
    class Meta:
        model = WorkDetail
        fields = ("department", "basic_salary", "employee_no",
                  "date_of_employment", "social_security_no")

    def __init__(self, employer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].queryset = Department.objects.filter(
            employer=employer)


class PaymentDetailForm(forms.ModelForm):
    class Meta:
        model = PaymentDetail
        fields = ("bonus", "allowances", "deductions")


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ("name", "description", "logo")

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name",)
