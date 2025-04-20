from django.db import models
from .leads import Lead
from .etapas import Etapas
from myapps.authentication.models import UserCustomize
from myapps.catalogos.models import InstitucionAcademica
# Create your models here.

class HistorialLeadInstitucion(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    institucion = models.ForeignKey(InstitucionAcademica, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    cambiado_por = models.ForeignKey(UserCustomize, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    