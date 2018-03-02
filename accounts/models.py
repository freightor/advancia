from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel

# Create your models here.


class Profile(models.Model):
    """
    Abstract Base Class for individuals in an employee with Login abilities
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_choices = (
        ("admin", "Admin"),
        ("regular", "Regular")
    )
    role = models.CharField(
        max_length=10, choices=role_choices, default="regular")

    class Meta:
        abstract = True
