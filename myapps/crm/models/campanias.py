from django.db import models
from .fuentes import Fuentes
from myapps.control_escolar.models import ProgramaEducativo
from myapps.catalogos.models import InstitucionAcademica


class Campania(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    # fuente = models.ForeignKey(Fuentes, on_delete=models.CASCADE, related_name="campanas")
    # presupuesto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    activa = models.IntegerField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class CampaniaPrograma(models.Model):
    campania = models.ForeignKey(Campania, on_delete=models.CASCADE, related_name="programa_campania")
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="campania_programa")
    unidad_academica = models.ForeignKey(InstitucionAcademica, on_delete=models.CASCADE, related_name="campanias_unidad", null=True, blank=True)
    costo_asignado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)