from django.db import models
from django.conf import settings
# Create your models here.

class Base(models.Model):
    class Meta:
        abstract = True
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_modified_by_related"
    )  

class TipoProducto(Base):
    name = models.CharField(max_length=50)
    requiere_produccion = models.IntegerField(default=0)
    incluye_hosting = models.IntegerField(default=0)
    es_recurrente = models.IntegerField(default=0)
    

class Producto(Base):
    name = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE, related_name="productos")
    costo_base = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # mensualidades = models.IntegerField(null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    descuento_monto = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    dias_entrega = models.PositiveBigIntegerField(default=3)
    
    estado = models.IntegerField(default=0)
#    catalogo
class Periodicidad(Base):
    DIAS = "days"
    SEMANAS = "weeks"
    MESES = "months"
    ANIOS = "years"
    UNIDAD_CHOICES = [
        (DIAS, "Días"),
        (SEMANAS, "Semanas"),
        (MESES, "Meses"),
        (ANIOS, "Años"),
    ]

    nombre = models.CharField(max_length=50, unique=True) 
    unidad = models.CharField(max_length=10, choices=UNIDAD_CHOICES, default=MESES)
    intervalo = models.PositiveIntegerField(default=1)     
    descripcion = models.TextField(blank=True, null=True)
    
# plan de pago
class PlanPago(Base):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="planes_pago")
    nombre = models.CharField(max_length=100) 
    periodicidad = models.ForeignKey(Periodicidad, on_delete=models.PROTECT, related_name="planes")
    numero_pagos = models.PositiveIntegerField(default=1)
    monto_por_periodo = models.DecimalField(max_digits=10, decimal_places=2)
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)

    incluye_factura = models.IntegerField(default=0)
    activo = models.IntegerField(default=0)

    def total_estimado(self):
        return (self.monto_por_periodo * self.numero_pagos) + (self.anticipo or 0)

    def __str__(self):
        return f"{self.nombre} - {self.producto}"