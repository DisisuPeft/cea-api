from django.db import models
from ...catalogos.models.materias import Materias
from ...catalogos.models.grupos import Grupos
from ...catalogos.models.ciclos import Ciclos
from myapps.maestros.models.maestro import Maestro

class Asignaciones(models.Model):
    profesor = models.ForeignKey(Maestro, on_delete=models.CASCADE, related_name="profesor_asignacion")
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_asignacion")
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE, related_name="grupo_asignacion")
    ciclo = models.ForeignKey(Ciclos, related_name="ciclo_asignacion", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)