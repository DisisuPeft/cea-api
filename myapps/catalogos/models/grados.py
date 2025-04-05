from django.db import models
from .niveles import Niveles

class Grados(models.Model):
    name = models.CharField(max_length=50)
    nivel = models.ForeignKey(Niveles, on_delete=models.CASCADE, related_name="nivel_grados")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)