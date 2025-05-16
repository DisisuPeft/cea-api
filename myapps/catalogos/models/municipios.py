from django.db import models
# from .subcategorias import SubCategory
from .estados_republica import EstadosRepublica

class Municipios(models.Model):
    nombre = models.CharField(max_length=100)
    clave = models.CharField(max_length=20, null=True, blank=True)
    activo = models.IntegerField(null=True, blank=True)
    estado = models.ForeignKey(EstadosRepublica, related_name="municipio", on_delete=models.SET_NULL, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(null=True, blank=True)