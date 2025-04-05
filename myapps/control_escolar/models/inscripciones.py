from django.db import models
from ...catalogos.models.grupos import Grupos
from ...catalogos.models.ciclos import Ciclos
from myapps.estudiantes.models.estudiante import Estudiante

class Inscripciones(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="estudiante_inscripciones")
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE, related_name="grupo_inscripcion")
    ciclo = models.ForeignKey(Ciclos, on_delete=models.CASCADE, related_name="periodos_inscripcion")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)