from django.db import models
from .materias import Materias
from .periodos import Periodos

class Especialidades(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)