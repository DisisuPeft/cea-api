from django.db import models
from myapps.catalogos.models import InstitucionAcademica
from myapps.sistema.models import Empresa
from myapps.control_escolar.models import ProgramaEducativo
# Create your models here.

class Pipline(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField()
    empresa = models.ForeignKey(Empresa, related_name="pipline", on_delete=models.CASCADE, null=True, blank=True)
    unidad_academica = models.ForeignKey(InstitucionAcademica, related_name="ua_pipline", on_delete=models.CASCADE, null=True, blank=True)
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.orden} - {self.nombre}"

    class Meta:
        ordering = ['orden']