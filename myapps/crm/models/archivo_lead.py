from django.db import models
from .leads import Lead
from .etapas import Etapas
from myapps.authentication.models import UserCustomize
# Create your models here.

class ArchivoLead(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='leads/archivos/')
    nombre = models.CharField(max_length=200)
    subido_por = models.ForeignKey(UserCustomize, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
