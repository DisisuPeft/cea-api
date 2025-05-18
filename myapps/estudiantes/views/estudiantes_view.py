from django.shortcuts import render
from contextvars import Token

from myapps.authentication.manager import CustomUserManager
from myapps.authentication.models import UserCustomize as User
from django.http import JsonResponse
from django.utils.decorators import method_decorator  # importante
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from myapps.perfil.serializer import ProfileSerializer
from myapps.estudiantes.serializer import EstudianteSerializer, EstudianteSerializerView, EstudianteEditSerializer

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf import settings
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.estudiantes.models import Estudiante
from django.utils import timezone
from django.db.models import Q

# Create your views here.
# EN formularios siempre devolver el puro serializer 
class StudentsView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    # select_related -- para relacion 1 a 1 y 1 a M // prefetch -- para many to many e inversa
    def get(self, request):
        estudiantes = Estudiante.objects.all()
        if not estudiantes:
            return Response("Estudiantes not found", status=status.HTTP_404_NOT_FOUND)
        serializer = EstudianteSerializerView(estudiantes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        # print(request.data)
        profile_req = request.data.pop('profile')
        user_req = {}
        student = {}
        if 'user' in request.data and request.data['user']:
            user_req = request.data.pop('user')
        profile = {}
        for key, value in profile_req.items():
            if value:
                profile[key] = profile_req[key]
        for key in request.data:
            if key in request.data and request.data[key]:
                student[key] = request.data[key]
        # print(student)
        profile_serializer = ProfileSerializer(data=profile) 
        if profile_serializer.is_valid():
            serializer_p = profile_serializer.save()
            student['perfil'] = serializer_p.id
            print(student)
            estudiante_serializer = EstudianteSerializer(data=student)
            if estudiante_serializer.is_valid():
                estudiante_serializer.save()
                # Aqui falta el usuario
                return Response("Estudiante creado con exito", status=status.HTTP_200_OK) 
            else:
                return Response(estudiante_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class StudentView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    # select_related -- para relacion 1 a 1 y 1 a M // prefetch -- para many to many e inversa
    def get(self, request, id):
        estudiante = Estudiante.objects.filter(id=id)
        if not estudiante:
            return Response("Estudiantes not found", status=status.HTTP_404_NOT_FOUND)
        serializer = EstudianteSerializerView(estudiante[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class StudentUpdateView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    # select_related -- para relacion 1 a 1 y 1 a M // prefetch -- para many to many e inversa
    def get(self, request, id):
        estudiante = Estudiante.objects.filter(id=id).select_related("lugar_nacimiento", "municipio")
        if not estudiante:
            return Response("Estudiantes not found", status=status.HTTP_404_NOT_FOUND)
        serializer = EstudianteEditSerializer(estudiante[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        if request.data and request.data['id']:
            estudiante = Estudiante.objects.get(id=request.data['id'])
            if not estudiante:
                return Response("Student not found", status=status.HTTP_404_NOT_FOUND)
            update_serializer = EstudianteSerializer(estudiante, data=request.data, partial=True)
            if update_serializer.is_valid():
                update_serializer.save()
                return Response("Usuario actualizado con exito", status=status.HTTP_200_OK)
            # return Response("test", status=status.HTTP_200_OK)
            else:
                return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response("The request is empty", status=status.HTTP_400_BAD_REQUEST)
        
    