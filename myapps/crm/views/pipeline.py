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
# from myapps.perfil.models import User
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf import settings
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from ..models import Pipline
from ..serializer import PipelineSerializer
from django.utils import timezone
from django.db.models import Q
# Create your views here.
# EN formularios siempre devolver el puro serializer 
# class PipelineAllView(APIView):
#     permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
#     authentication_classes = [CustomJWTAuthentication]
    
#     def get(self, request):
        
#         pipeline = Pipline.objects.all().select_related('etapas')
        
#         if not pipeline:
#             return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        
#         serializer = PipelineSerializer(pipeline[0])
#         return Response(serializer.data, status=status.HTTP_200_OK)
    