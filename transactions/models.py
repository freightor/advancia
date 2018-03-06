from django.db import models
from common.models import BaseModel
from employers.models import Employee
from stores.models import Store

# Create your models here.
class Transaction(BaseModel):
    amount = models.DecimalField(default=0)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("initiated","Initiated"),
        ("pending","Pending"),
        ("verified","Verified"),
        ("completed","Completed")
    )
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="initiated")