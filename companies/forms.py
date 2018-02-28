from django import forms
from companies.models import Employee, Employer, Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("location", "postal_address", "phone", "email")


class EmployeeForm(forms.ModelForm):
    user_type = forms.CharField(widget=forms.HiddenInput, initial="employee")

    class Meta:
        model = Employee
        fields = ("avatar", "role", "salary", "employee_no")


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ("name", "description", "logo")
