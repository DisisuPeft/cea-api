from django.db import models
from .categorias import Categoria

class SubCategoria(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, related_name="subcategory", null=True
    )
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)