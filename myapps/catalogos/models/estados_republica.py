from django.db import models
# from .subcategorias import SubCategory

class EstadosRepublica(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)