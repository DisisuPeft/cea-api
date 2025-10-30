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

class Comentario(Base):
    comentario = models.TextField(max_length=500)
    diplomado = models.ForeignKey('control_escolar.ProgramaEducativo', on_delete=models.CASCADE, related_name="comentarios",
        null=True, blank=True
    )
    modulo = models.ForeignKey("control_escolar.ModuloEducativo", on_delete=models.CASCADE, related_name="comentarios",
        null=True, blank=True
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="comentarios")
    padre = models.ForeignKey("self", on_delete=models.CASCADE, 
        null=True, blank=True, related_name="respuestas"
    )

    editado = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=["diplomado", "-fecha_creacion"]),
            models.Index(fields=["modulo", "-fecha_creacion"]),
            models.Index(fields=["usuario", "-fecha_creacion"])
        ]
        ordering = ["-fecha_creacion"]

class PlataformasImparticion(Base):
    nombre = models.CharField(max_length=50) 
        
class EnlaceClase(Base):
    programa = models.ForeignKey('control_escolar.ProgramaEducativo', on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=255)
    fecha_imparticion = models.DateField()
    titulo = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    plataforma = models.ForeignKey(PlataformasImparticion, on_delete=models.CASCADE, blank=True, null=True)
    password_platform = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        ordering = ["-fecha_imparticion"]
        indexes = [
            models.Index(fields=["programa", "-fecha_imparticion"])
        ]
        
        
class ComentarioVisto(Base):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='vistas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios_vistos')
    visto_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comentario', 'usuario')
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['comentario', 'usuario']),
        ]
        



