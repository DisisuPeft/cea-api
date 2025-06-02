from rest_framework import serializers
from ..models import Estatus


class EstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estatus
        fields = ["id", "nombre"]
        
        
    def create(self, validated_data):
        estatus = Estatus.objects.create(**validated_data)
        if not estatus:
            raise serializers.ValidationError("El estatus no fue creado")
        return estatus
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance