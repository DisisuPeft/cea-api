from django.db import models
from .preguntas import Preguntas

class OpcionesRespuestas(models.Model):
    pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE, related_name="respuesta")
    text = models.TextField()
    is_correct = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)