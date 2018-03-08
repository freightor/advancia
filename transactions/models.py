from django.db import models
from common.models import BaseModel
from employers.models import Employee
from stores.models import Store
from common.utils import make_ref

# Create your models here.
class Transaction(BaseModel):
    reference_code = models.CharField(max_length=32,unique=True,default=make_ref)
    amount = models.DecimalField(default=0,max_digits=12,decimal_places=2)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=50,null=True,blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("initiated","Initiated"),
        ("pending","Pending"),
        ("verified","Verified"),
        ("completed","Completed")
    )
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="initiated")