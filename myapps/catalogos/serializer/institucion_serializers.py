from rest_framework import serializers
from ..models import InstitucionAcademica

class InstitucionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitucionAcademica
        fields = ["id", "nombre", "descripcion", "sitio_web", "telefono", "email_contacto", "direccion", "responsable", "activa", "fecha_creacion", "fecha_actualizacion"]