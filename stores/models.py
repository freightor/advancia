import os
import uuid
from django.db import models
from accounts.models import Profile
from employers.models import Address
from common.models import BaseModel, ActiveModel
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

# Create your models here.


class Store(BaseModel, ActiveModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True,blank=True)


def storeuser_avatar(instance, filename):
    file_ext = os.path.splitext(filename)[1]
    return "stores/{0}{1}".format(uuid.uuid1().hex, file_ext)


class StoreUser(BaseModel,Profile):
    store = models.ForeignKey(Store, on_delete=models.CASCADE,null=True,blank=True)
    avatar = models.ImageField(upload_to=storeuser_avatar,null=True,blank=True)

@receiver(post_save, sender=StoreUser)
def generate_store_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance.user)