from myapps.authentication.models import UserCustomize, Roles, Permissions
from rest_framework import serializers
from myapps.perfil.models import User
from myapps.perfil.serializer import ProfileSerializer
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions
from myapps.sistema.models.modulo import Modulos
from myapps.sistema.models.tabs_module import TabsModulo
from myapps.authentication.serializers import RoleCustomizeSerializer, PermissionCustomizeSerializer, UserCustomizeSerializer

class ModulosSerializer(serializers.ModelSerializer):
    # role = RoleCustomizeSerializer(many=True, required=False)
    class Meta:
        model = Modulos
        fields = ["id", "name", "icon","bgColor", "textColor", "route"]
        

        
        
        
        
        
class PlataformaModuloSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    module = serializers.IntegerField(required=False)
    user = serializers.IntegerField(required=False)
    tabmodule = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=True,
        required=False
    )
    
    class Meta:
        model = Modulos
        fields = ['id', 'name', "module", "tabmodule", "user"]
        
    def create(self, validated_data):
        tabsmodule = validated_data.get("tabmodule") or []
        user = validated_data.get("user", None)
        module = validated_data.get("module", None)
        print(user)
        modulo = Modulos.objects.get(id=module)
        if not modulo:
            raise serializers.ValidationError("module not found")
            
        modulo.usuario.add(user)
        
        tabs = TabsModulo.objects.filter(modulo__id=modulo.id).filter(id__in=tabsmodule)
        
        # print(tabs)      
        for tab in tabs:
            tab.user.add(user)
        
        # print(modulo, tabs)
        return modulo
        
        
class PestaniaPlataformaSerializer(serializers.ModelSerializer):
    # modulo = ModulosSerializer(required=False)
    # permiso = PermissionCustomizeSerializer(many=True, required=False)
    # user = UserCustomizeSerializer(many=True, required=False)
    class Meta:
        model = TabsModulo
        fields = ["id", "name", "href", "icon"]

    
class TabsModuloSerializer(serializers.ModelSerializer):
    modulo = ModulosSerializer(required=False)
    permiso = PermissionCustomizeSerializer(many=True, required=False)
    # user = UserCustomizeSerializer(many=True, required=False)
    class Meta:
        model = TabsModulo
        fields = ["id", "name", "description", "modulo", "permiso", "href", "icon", "orden"]


