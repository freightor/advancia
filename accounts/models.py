from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    user_types_choices = (
        ("merchant", "Merchant"),
        ("employee", "Employee")
    )
    user_type = models.CharField(max_length=10, choices=user_types_choices)
    role_choices = (
        ("admin", "Admin"),
        ("regular", "Regular")
    )
    role = models.CharField(
        max_length=10, choices=role_choices, default="regular")

    class Meta:
        abstract = True
