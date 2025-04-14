from django.db import models
from .materias import Materias
from .grupos import Grupos
from .ciclos import Ciclos

class TipoNivel(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)