from django.db import models
from myapps.catalogos.models import InstitucionAcademica
from myapps.authentication.models import UserCustomize

class TipoPrograma(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
class ModalidadesPrograma(models.Model):
    name = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    sincronia = models.CharField(max_length=200, blank=True, null=True) 
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class ProgramaEducativo(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.ForeignKey(TipoPrograma, on_delete=models.CASCADE, related_name="programas", blank=True, null=True)
    institucion = models.ForeignKey(InstitucionAcademica, on_delete=models.CASCADE, related_name="programas", blank=True, null=True)
    duracion_horas = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    
    horario = models.CharField(max_length=200, blank=True, null=True)  # ej. Sábados y Domingos de 8 a 14 hrs
    costo_inscripcion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_mensualidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    activo = models.IntegerField()
    maestro = models.ForeignKey(UserCustomize, on_delete=models.CASCADE, related_name="programas", null=True, blank=True)
    modalidad = models.ForeignKey(ModalidadesPrograma, on_delete=models.CASCADE, related_name="modalidades_programas", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
    
class Dirigido(models.Model):
    nombre = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="dirigido")
    
class PublicoObjetivo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name='publicos_objetivo')
    
class PerfilIngreso(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="perfiles_ingreso")
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class RequisitoActitudinal(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisitos_actitudinales")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class RequisitoDeseable(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisitos_deseables")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class EnfoquePedagogico(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="enfoques_pedagogicos")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class RequisitoIngreso(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisitos_ingreso")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class RequisitoPermanencia(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisitos_permanencia")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class RequisitoEgreso(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisitos_egreso")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class PerfilEgreso(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="perfil_egreso")
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class ResultadoAplicacion(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="resultados_aplicacion")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class ResultadoActualizacion(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="resultados_actualizacion")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class ResultadoCrecimiento(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="resultados_crecimiento")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class JustificacionPrograma(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="justificacion")
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class ModuloEducativo(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="modulos")
    nombre = models.CharField(max_length=300)
    
    horas_teoricas = models.IntegerField()
    horas_practicas = models.IntegerField()
    horas_totales = models.IntegerField()
    creditos = models.DecimalField(max_digits=4, decimal_places=2)
    
class CalendarioModulo(models.Model):
    modulo = models.ForeignKey(ModuloEducativo, on_delete=models.CASCADE, related_name="calendarios")
    periodo = models.CharField(max_length=100)
    numero_horas = models.IntegerField()
    numero_semanas = models.IntegerField()
    
class SubModulo(models.Model):
    modulo = models.ForeignKey(ModuloEducativo, on_delete=models.CASCADE, related_name="submodulos")
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.IntegerField(default=0)