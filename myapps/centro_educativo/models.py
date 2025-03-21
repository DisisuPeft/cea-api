from django.db import models
from myapps.authentication.models import UserCustomize
from myapps.perfil.models import Profile
# Create your models here.
# Niveles y grupos
class Niveles(models.Model):
    name = models.CharField(max_length=50)
    
class Grados(models.Model):
    name = models.CharField(max_length=50)
    nivel = models.ForeignKey(Niveles, on_delete=models.CASCADE, related_name="nivel_grados")
    
class Grupos(models.Model):
    name = models.CharField(max_length=50)
    grado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name="grado_grupos")
    
class Estuidantes(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(Profile, related_name="estudiante", on_delete=models.CASCADE)
    

# Ciclos y periodos
class Ciclos(models.Model):
    name = models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

class Periodos(models.Model):
    name = models.CharField(max_length=20)
    ciclo = models.ForeignKey(Ciclos, on_delete=models.CASCADE, related_name="periodos")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
class Inscripciones(models.Model):
    estudiante = models.ForeignKey(Estuidantes, on_delete=models.CASCADE, related_name="estudiante_inscripciones")
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE, related_name="grupo_inscripcion")
    ciclo = models.ForeignKey(Ciclos, on_delete=models.CASCADE, related_name="periodos_inscripcion")
    
class PadresFamilia(models.Model):
    name = models.CharField(max_length=50)
    apellidoP = models.CharField(max_length=50)
    apellidoM = models.CharField(max_length=50)
    estudiantes = models.ManyToManyField(Estuidantes, related_name="estudiante_padres")
    
class Materias(models.Model):
    name = models.CharField(max_length=100)
    grado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name="materias_grado")
    
class Profesores(models.Model):
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="perfil_profesor")
    
class Asignaciones(models.Model):
    profesor = models.ForeignKey(Profesores, on_delete=models.CASCADE, related_name="profesor_asignacion")
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_asignacion")
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE, related_name="grupo_asignacion")
    ciclo = models.ForeignKey(Ciclos, related_name="ciclo_asignacion", on_delete=models.CASCADE)
    
class Calificaciones(models.Model):
    estudiante = models.ForeignKey(Estuidantes, on_delete=models.CASCADE, related_name="estudiante_calificacion")
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_calificacion")
    periodo = models.ForeignKey(Periodos, on_delete=models.CASCADE, related_name="periodo_calificacion")
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)

class Asistencias(models.Model):
    estudiante = models.ForeignKey(Estuidantes, on_delete=models.CASCADE, related_name="estudiante_asistencia")
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_asistencia")
    fecha = models.DateField()
    state = models.BigIntegerField()

class TiposExamen(models.Model):
    name = models.CharField(max_length=50)
    
class Examenes(models.Model):
    name = models.CharField(max_length=100)
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_examenes")
    periodo = models.ForeignKey(Periodos, on_delete=models.CASCADE, related_name="periodo_examenes")
    tipo_examen = models.ForeignKey(TiposExamen, on_delete=models.CASCADE, related_name="tipo_examen")
    fecha = models.DateField()
    
class CalificacionesExamen(models.Model):
    estudiante = models.ForeignKey(Estuidantes, on_delete=models.CASCADE, related_name="estudiante_examen")
    examen = models.ForeignKey(Examenes, on_delete=models.CASCADE, related_name="examen_calificacion")
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    
class TipoPreguntas(models.Model):
    name = models.CharField(max_length=50)
    
class Preguntas(models.Model):
    examen = models.ForeignKey(Examenes, on_delete=models.CASCADE, related_name="examen")
    enunciado = models.TextField()
    tipo = models.ForeignKey(TipoPreguntas, on_delete=models.CASCADE, related_name="tipo")
    
class OpcionesRespuestas(models.Model):
    pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE, related_name="respuesta")
    text = models.TextField()
    is_correct = models.IntegerField()
    
class RespuestasEstudiantes(models.Model):
    estudiante = models.ForeignKey(Estuidantes, on_delete=models.CASCADE, related_name="estudiante_respuesta")
    pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE, related_name="pregunta_respuesta")
    respuesta = models.TextField()
    
class Matriculas(models.Model):
    estudiante = models.ForeignKey(Estuidantes, on_delete=models.CASCADE, related_name="estudiante_matricula")
    nivel = models.ForeignKey(Niveles, on_delete=models.CASCADE, related_name="nivel_matricula")
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE, related_name="grupo_matricula")
    ciclo = models.ForeignKey(Ciclos, related_name="ciclo_matricula", on_delete=models.CASCADE)
    grado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name="grado_matricula")
    state = models.BigIntegerField()