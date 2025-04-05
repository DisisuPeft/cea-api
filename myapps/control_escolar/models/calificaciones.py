from django.db import models
from ...catalogos.models.materias import Materias
from ...catalogos.models.periodos import Periodos
from myapps.estudiantes.models.estudiante import Estudiante

class Calificaciones(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="estudiante_calificacion")
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_calificacion")
    periodo = models.ForeignKey(Periodos, on_delete=models.CASCADE, related_name="periodo_calificacion")
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)