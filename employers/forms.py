from django import forms
from employers.models import Employee, Employer, Address, WorkDetail, PaymentDetail, Department, Administrator


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("location", "postal_address", "phone", "email")


class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ("avatar", "role")


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("first_name", "middle_name", "last_name","headshot",
                  "date_of_birth", "gender", "marital_status")


class WorkDetailForm(forms.ModelForm):
    class Meta:
        model = WorkDetail
        fields = ("department", "basic_salary",
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
    PAYROLL_DATE_CHOICES = [
        (i,str(i)) for i in range(1,30)
    ]
    payroll_date = forms.TypedChoiceField(choices=PAYROLL_DATE_CHOICES,initial=29, coerce=int)
    class Meta:
        model = Employer
        fields = ("name", "description", "logo","payroll_date")


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name",)

class FileUploadForm(forms.Form):
    upload_file = forms.ClearableFileInput()