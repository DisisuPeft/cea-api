from django.db import models
from django.utils import timezone
from django.conf import settings
from myapps.sistema.models import Empresa

class Base(models.Model):
    class Meta:
        abstract = True
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_modified_by_related"
    )
    empresa = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_empresa_related"
    )
    
class Base1(Base):
    class Meta:
        abstract = True
        
    institucion = models.ForeignKey("catalogos.InstitucionAcademica", 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="%(app_label)s_%(class)s_unidad_related"
    )
        
    