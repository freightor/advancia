from django.db import models
from accounts.models import Profile
from common.models import BaseModel, ActiveModel

# Create your models here.


class Store(BaseModel, ActiveModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class StoreUser(Profile):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
