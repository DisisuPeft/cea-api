from django.db import models
from myapps.catalogos.models import Ciclos, InstitucionAcademica
from .programa_educativo import ModalidadesPrograma


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=50)
    estatus = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    
class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    ciclo = models.ForeignKey(Ciclos, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    institucion = models.ForeignKey(InstitucionAcademica, on_delete=models.CASCADE, null=True, blank=True)
    modalidad = models.ForeignKey(ModalidadesPrograma, on_delete=models.SET_NULL, related_name="evento", null=True, blank=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name="evento")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True) 