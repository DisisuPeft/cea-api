from django.db import models
from .leads import Lead
from .etapas import Etapas
from myapps.authentication.models import UserCustomize
# Create your models here.

class HistorialEtapa(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='historial_etapas')
    etapa = models.ForeignKey(Etapas, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    cambiado_por = models.ForeignKey(UserCustomize, on_delete=models.CASCADE, null=True)
    
    class Meta:
        ordering = ['-fecha_entrada']