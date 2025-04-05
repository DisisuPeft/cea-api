from django.db import models
from .preguntas import Preguntas
from myapps.estudiantes.models.estudiante import Estudiante

class RespuestasEstudiantes(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="estudiante_respuesta")
    pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE, related_name="pregunta_respuesta")
    respuesta = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)