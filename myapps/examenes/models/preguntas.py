from django.db import models
from .tipo_pregunta import TipoPreguntas
from .examen import Examenes

class Preguntas(models.Model):
    examen = models.ForeignKey(Examenes, on_delete=models.CASCADE, related_name="preguntas_examen")
    enunciado = models.TextField()
    tipo = models.ForeignKey(TipoPreguntas, on_delete=models.CASCADE, related_name="preguntas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)