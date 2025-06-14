from django.db import models
from .pipline import Pipline
# Create your models here.

class Estatus(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    pipeline = models.ForeignKey(Pipline, on_delete=models.CASCADE, related_name="estatus", null=True, blank=True)