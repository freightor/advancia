from django import forms
from companies.models import Employee, Employer, Address, WorkDetail, PaymentDetail, Department


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("location", "postal_address", "phone", "email")


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("first_name", "middle_name", "last_name",
                  "date_of_birth", "gender", "marital_status")


class WorkDetailForm(forms.ModelForm):
    class Meta:
        model = WorkDetail
        fields = ("department", "salary", "employee_no",
                  "date_of_employment", "social_security_no")

    def __init__(self, company, *args, **kwargs):
        self.fields["department"].queryset = Department.objects.filter(
            company=company)
        super().__init__(*args, **kwargs)


class PaymentDetailsForm(forms.ModelForm):
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
        fields = ("name")