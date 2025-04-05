from django.db import models
# Create your models here.

class Etapas(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.orden} - {self.nombre}"

    class Meta:
        ordering = ['orden']