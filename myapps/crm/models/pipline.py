from django.db import models
# Create your models here.

class Pipline(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.orden} - {self.nombre}"

    class Meta:
        ordering = ['orden']