from django.db import models
from .tipo_nivel import TipoNivel

class NivelEducativo(models.Model):
    name = models.CharField(max_length=50)
    tipo_nivel = models.ForeignKey(TipoNivel, on_delete=models.CASCADE, related_name="niveles", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)