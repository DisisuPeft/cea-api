from django.db import models
from .pipline import Pipline
# Create your models here.

class Etapas(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField()
    pipline = models.ForeignKey(Pipline, on_delete=models.CASCADE, related_name="etapas", null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.orden} - {self.nombre}"

    class Meta:
        ordering = ['orden']