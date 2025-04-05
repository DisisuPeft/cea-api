from django.db import models
from .grados import Grados

class Grupos(models.Model):
    name = models.CharField(max_length=50)
    grado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name="grado_grupos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)