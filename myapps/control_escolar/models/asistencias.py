from django.db import models
from ...catalogos.models.materias import Materias
from myapps.estudiantes.models.estudiante import Estudiante

class Asistencias(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="estudiante_asistencia")
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_asistencia")
    fecha = models.DateField()
    state = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)