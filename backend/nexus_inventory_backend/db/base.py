# Internal
import uuid

# Django
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50, blank=True)
    deleted = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=50, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True
