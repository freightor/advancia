from django.db import models
from django.contrib.auth.models import User

# Base Model for shared items in all Models


class BaseModel(models.Model):
    edited_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_%(class)s", related_query_name="created_%(class)ss", null=True, blank=True)
    edited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="edited_%(class)s", related_query_name="created_%(class)ss", null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self,"name"):
            return self.name
        if hasattr(self,"user"):
            return self.user.get_full_name()
        if hasattr(self,"reference_code"):
            return self.reference_code

class ActiveModel(models.Model):
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True
