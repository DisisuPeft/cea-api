from django.db import models
from myapps.authentication.models import UserCustomize as User
from .observaciones import Observaciones
from .estatus import Estatus
from .fuentes import Fuentes
from .etapas import Etapas
from .notas import Notas
# Create your models here.

class Lead(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fuente = models.ForeignKey(Fuentes, on_delete=models.CASCADE, related_name="fuente")
    interesado_en = models.CharField(max_length=200, blank=True)
    etapa = models.ForeignKey(Etapas, on_delete=models.CASCADE, related_name="etapa")
    estatus = models.ForeignKey(Estatus, on_delete=models.CASCADE, related_name="estatus")
    observaciones = models.ForeignKey(Observaciones, on_delete=models.CASCADE, related_name="obs")
    vendedor_asignado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='leads_asignados')
    notas = models.ManyToManyField(Notas, related_name="notas")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)