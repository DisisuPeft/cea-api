from django.db import models
# Create your models here.

class Fuentes(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey('sistema.Empresa', on_delete=models.SET_NULL, related_name="fuentes_crm", blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
