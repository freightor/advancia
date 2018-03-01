from django.contrib import admin
from employers.models import Employee, Employer, Address, WorkDetail,PaymentDetail,Payroll

# Register your models here.
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Address)
admin.site.register(WorkDetail)
admin.site.register(PaymentDetail)
admin.site.register(Payroll)
