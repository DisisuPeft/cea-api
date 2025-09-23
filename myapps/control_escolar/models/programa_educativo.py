from django.db import models
from myapps.catalogos.models import InstitucionAcademica
from myapps.authentication.models import UserCustomize
from myapps.maestros.models import Maestro
from myapps.catalogos.models import Ciclos, Periodos
from myapps.estudiantes.models import Estudiante

class TipoPrograma(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
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
    # ciclo = models.ForeignKey(Ciclos, on_delete=models.SET_NULL, related_name="programa_educativo", null=True, blank=True)
    periodo_imparticion = models.ForeignKey(Periodos, on_delete=models.SET_NULL, related_name="programa_educativo", null=True, blank=True)
    horario = models.CharField(max_length=200, blank=True, null=True)  # ej. Sábados y Domingos de 8 a 14 hrs
    costo_inscripcion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_mensualidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    inscripcion = models.ManyToManyField(Estudiante, related_name="program", null=True, blank=True)
    activo = models.IntegerField()
    maestro = models.ManyToManyField(Maestro, related_name="programas", null=True, blank=True)
    modalidad = models.ForeignKey(ModalidadesPrograma, on_delete=models.CASCADE, related_name="programas", null=True, blank=True)
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
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name='publico_objetivo')
    
class PerfilIngreso(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="perfil_ingreso")
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=0)
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
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="enfoque_pedagogico")
    texto = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class RequisitoIngreso(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisito_ingreso")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class RequisitoPermanencia(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisito_permanencia")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class RequisitoEgreso(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisito_egreso")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class PerfilEgreso(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="perfil_egreso")
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class ResultadoAplicacion(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="resultado_aplicacion")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class ResultadoActualizacion(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="resultado_actualizacion")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

class ResultadoCrecimiento(models.Model):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="resultado_crecimiento")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)
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
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class CalendarioModulo(models.Model):
    modulo = models.ForeignKey(ModuloEducativo, on_delete=models.CASCADE, related_name="calendario_modulo")
    periodo = models.CharField(max_length=100)
    numero_horas = models.IntegerField()
    numero_semanas = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class SubModulo(models.Model):
    modulo = models.ForeignKey(ModuloEducativo, on_delete=models.CASCADE, related_name="submodulos")
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.IntegerField(default=0)
    path_class = models.CharField(null=True, blank=True, max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class TypeFile(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
class MaterialModulos(models.Model):
    file = models.FileField(upload_to="materiales/")
    modulo = models.ForeignKey(ModuloEducativo, on_delete=models.CASCADE, related_name="materiales", null=True, blank=True)
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.SET_NULL, related_name="materiales", null=True, blank=True)
    submodulo = models.ForeignKey(SubModulo, on_delete=models.CASCADE, related_name="materiales", null=True, blank=True)
    type = models.ForeignKey(TypeFile, on_delete=models.CASCADE, related_name="material", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)