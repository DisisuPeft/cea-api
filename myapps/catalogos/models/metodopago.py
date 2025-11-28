from django.db import models
# from myapps.control_escolar.models import Base
from django.conf import settings

class Base(models.Model):
    class Meta:
        abstract = True
        
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_modified_by_related"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_owner_by_related",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

class MetodoPago(Base):
    nombre = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)
    