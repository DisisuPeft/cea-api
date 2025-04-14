from django.db import models
from ...catalogos.models.materias import Materias
from ...catalogos.models.periodos import Periodos
from .tipo_examen import TiposExamen

class Examenes(models.Model):
    name = models.CharField(max_length=100)
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_examenes")
    periodo = models.ForeignKey(Periodos, on_delete=models.CASCADE, related_name="periodo_examenes")
    tipo_examen = models.ForeignKey(TiposExamen, on_delete=models.CASCADE, related_name="tipo_examen")
    fecha = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)