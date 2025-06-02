from rest_framework import serializers
from ..models import Fuentes

class FuenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuentes
        fields = ["id", "nombre"]

    def create(self, validated_data):
        fuentes = Fuentes.objects.create(**validated_data)
        if not fuentes:
            raise serializers.ValidationError("Las fuentes no fueron creadas")
        return fuentes
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance