from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from myapps.estudiantes.serializer import EstudianteSerializer, EstudianteSerializerView, EstudianteEditSerializer
from myapps.authentication.decorators import role_required
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from myapps.perfil.serializer import ProfileSerializer
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.estudiantes.models import Estudiante

class StudentUpdateProfile(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    # select_related -- para relacion 1 a 1 y 1 a M // prefetch -- para many to many e inversa
    def get(self, request, id):
        # print(id)
        estudiante = Estudiante.objects.filter(user__id=id).first()
        # print(estudiante)
        if not estudiante:
            return Response("Estudiantes not found", status=status.HTTP_404_NOT_FOUND)
        serializer = EstudianteSerializer(estudiante)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        # profile = {}
        if request.data and id:
            estudiante = Estudiante.objects.get(user__id=id)

            print(request.data['perfil'])
            update_serializer = EstudianteSerializer(estudiante, data=request.data, partial=True)
            # print(update_serializer.data)   
            if update_serializer.is_valid():
                update_serializer.save()
                return Response("Perfil actualizado con exito", status=status.HTTP_200_OK)
            # return Response("test", status=status.HTTP_200_OK)
            else:
                return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: 
            # print(estudiante)
            return Response("server response", status=status.HTTP_200_OK)