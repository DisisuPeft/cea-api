from django.db import models
from myapps.authentication.models import UserCustomize
from .modulo import Modulos

# Create your models here.


class AsignacionAcceso(models.Model):
    usuario = models.ForeignKey(UserCustomize, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulos, on_delete=models.CASCADE)
    otorgado_por = models.ForeignKey(UserCustomize, related_name="asignaciones_realizadas", on_delete=models.SET_NULL, null=True)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True)