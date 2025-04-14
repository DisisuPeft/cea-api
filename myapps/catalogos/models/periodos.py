from django.db import models
from .ciclos import Ciclos

class Periodos(models.Model):
    name = models.CharField(max_length=20)
    ciclo = models.ForeignKey(Ciclos, on_delete=models.CASCADE, related_name="periodos")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)