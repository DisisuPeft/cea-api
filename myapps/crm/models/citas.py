from django.db import models
from .leads import Lead
from myapps.authentication.models import UserCustomize

class TipoCita(models.Model):
    name = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class EstadoCita(models.Model):
    name = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class Cita(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="citas")
    responsable = models.ForeignKey(UserCustomize, on_delete=models.SET_NULL, null=True, related_name="citas_agendadas")
    tipo = models.ForeignKey(TipoCita, on_delete=models.CASCADE, related_name="tipo_cita")
    fecha = models.DateField()
    hora = models.TimeField()
    notas = models.TextField(blank=True, null=True)
    estado = models.ForeignKey(EstadoCita, on_delete=models.CASCADE, related_name="estado_cita")
    recordatorio_enviado = models.BooleanField(default=False)
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(null=True, blank=True)

    # def __str__(self):
    #     return f"Cita con {self.lead.nombre} el {self.fecha} a las {self.hora}" 