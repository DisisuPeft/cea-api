from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime, date
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
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
        verbose_name=("Owner"),
        related_name="%(app_label)s_%(class)s_owner_related",
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
    
    
    
class Estatus(Base):
    name = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name="Nombre"
    )
    


class Evento(Base):
    name = models.CharField(
        "Nombre", max_length=50, db_index=True
    )
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    fecha_evento = models.DateField("Fecha del evento", null=True, blank=True)
    hora_evento = models.TimeField("Hora del evento", null=True, blank=True)
    precio_venta = models.DecimalField(
        "Precio de venta", max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    fecha_contrato = models.DateField(null=True, blank=True)

    estatus = models.ForeignKey(
        Estatus, 
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="eventos", verbose_name="Estatus"
    )

    tipo_producto = models.ForeignKey(
        TipoProducto, 
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="eventos"
    )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        indexes = [
            models.Index(fields=["fecha_evento", "hora_evento"]),
        ]
        # ordering = ("-fecha_evento", "-fecha_actualizacion")

    def __str__(self):
        return self.name


class ItinerarioPaso(Base):
        evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="pasos")
        titulo = models.CharField(max_length=120)
        descripcion = models.TextField(blank=True)
        orden = models.PositiveIntegerField(default=1)
        include_password = models.IntegerField(default=0)
        password = models.CharField(max_length=50, null=True, blank=True)
        password_match = models.IntegerField(null=True, blank=True)
        # Desbloqueo por tiempo (dos formas):
        release_at = models.DateTimeField(null=True, blank=True)  # fecha/hora exacta
        # o relativo al evento:
        offset_minutes = models.IntegerField(default=0)  # p.ej. -10080 = 7 días antes, +120 = 2 h después
        paso = models.CharField(max_length=10, null=True, blank=True)
        url_map = models.SlugField(max_length=500, blank=True, null=True)
        hour = models.TimeField(blank=True, null=True)
        
        class Meta:
            ordering = ["orden"]

        def get_release_at(self):
            if self.release_at:
                return self.release_at
            
            fecha_evento = self.evento.fecha_evento
            
            # Si es date, conviértelo a datetime
            if isinstance(fecha_evento, date) and not isinstance(fecha_evento, datetime):
                fecha_datetime = datetime.combine(fecha_evento, datetime.min.time())
                fecha_datetime = timezone.make_aware(fecha_datetime)
            else:
                # Ya es datetime
                fecha_datetime = fecha_evento
                if timezone.is_naive(fecha_datetime):
                    fecha_datetime = timezone.make_aware(fecha_datetime)
            
            return fecha_datetime + timedelta(minutes=self.offset_minutes)

        def is_unlocked(self, now=None):
            now = now or timezone.now()
            return now >= self.get_release_at()