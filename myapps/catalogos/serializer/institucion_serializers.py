from rest_framework import serializers
from ..models import InstitucionAcademica

class InstitucionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitucionAcademica
        fields = '__all__'