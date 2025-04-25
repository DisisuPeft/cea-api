from django.db import models
from myapps.authentication.models import UserCustomize
from .leads import Lead
# Create your models here.

class Notas(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='notas', null=True)
    texto = models.TextField()
    usuario = models.ForeignKey(UserCustomize, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
