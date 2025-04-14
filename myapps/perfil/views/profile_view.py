from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from myapps.authentication.decorators import role_required
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from myapps.perfil.serializer import ProfileSerializer

class ProfileView(APIView):
    permission_classes = [HasRoleWithRoles(['Administrador', 'Docente', 'Estudiante']), IsAuthenticated]
    def get(self, request):
        user_id = request.GET.get('id')
        user = UserCustomize.objects.get(id=user_id)
        if not user:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserCustomizeSerializer(user)
        # serializer.data.pop('roleID', [])
        #sera algo temporal
        profile_user = serializer.data.pop("profile")
        # print(profile_user)
        return Response({"profile": profile_user}, status=status.HTTP_200_OK)

    def patch(self, request):
        user_id = request.GET.get('id')
        profile_dict = {}
        user = UserCustomize.objects.get(id=user_id)
        profile = user.profile
        if not user:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        #actualizamos al usuario
        # if 'email' in request.data and request.data['email']:
        #     user.email = request.data['email']
        # if 'password' in request.data and request.data['password']:
        #     user.set_password(request.data['password'])
        
        # user.save()
        profile_fields = [
            "nombre", "apellidoP", "apellidoM", "edad", 
            "fechaNacimiento", "genero", "nivEdu", "telefono"
        ]

        for field in profile_fields:
            if field in request.data and request.data[field]:
                profile_dict[field] = request.data[field]
        serializer = ProfileSerializer(profile, data=profile_dict, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer = UserCustomizeSerializer(user)
            profile_updated = serializer.data.pop('profile')      
            return Response({"newprofile": profile_updated}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)