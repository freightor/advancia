from django.contrib import admin
from companies.models import Employee, Employer, Address

# Register your models here.
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Address)
