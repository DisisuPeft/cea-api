from django.db import models
from ...catalogos.models.materias import Materias
from ...catalogos.models.grupos import Grupos
from ...catalogos.models.ciclos import Ciclos

class TipoPreguntas(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)