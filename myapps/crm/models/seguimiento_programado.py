from django.db import models
from .leads import Lead
from .etapas import Etapas
from myapps.authentication.models import UserCustomize
# Create your models here.

class SeguimientoProgramado(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='seguimientos')
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    responsable = models.ForeignKey(UserCustomize, on_delete=models.CASCADE)
    completado = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
