from django.db import models
from .grados import Grados

class Materias(models.Model):
    name = models.CharField(max_length=100)
    grado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name="materias_grado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)