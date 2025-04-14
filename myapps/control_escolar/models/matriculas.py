from django.db import models
from ...catalogos.models.materias import Materias
from ...catalogos.models.niveles import Niveles
from ...catalogos.models.grupos import Grupos
from ...catalogos.models.ciclos import Ciclos
from ...catalogos.models.grados import Grados
from myapps.estudiantes.models.estudiante import Estudiante

class Matriculas(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="estudiante_matricula")
    nivel = models.ForeignKey(Niveles, on_delete=models.CASCADE, related_name="nivel_matricula")
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE, related_name="grupo_matricula")
    ciclo = models.ForeignKey(Ciclos, related_name="ciclo_matricula", on_delete=models.CASCADE)
    grado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name="grado_matricula")
    status = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)