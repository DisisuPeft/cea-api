from django.db import models
from .subcategorias import SubCategoria

class Especification(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(
        SubCategoria, on_delete=models.SET_NULL, related_name="especification", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)