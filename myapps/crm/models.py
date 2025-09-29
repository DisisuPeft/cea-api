from django.db import models
from django.utils import timezone
from django.conf import settings

class Base(models.Model):
    class Meta:
        abstract = True
    
    creation_date = models.DateTimeField(
        default=timezone.now(),
    )
    update_date = models.DateTimeField(
        auto_now=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
        related_name="owner_field",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="modifie_field",
    )