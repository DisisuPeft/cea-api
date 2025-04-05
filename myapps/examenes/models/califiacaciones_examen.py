from django.db import models
from .examen import Examenes
from myapps.estudiantes.models.estudiante import Estudiante

class CalificacionesExamen(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="estudiante_examen")
    examen = models.ForeignKey(Examenes, on_delete=models.CASCADE, related_name="examen_calificacion")
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)