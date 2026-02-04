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
from myapps.authentication.serializers import UserCustomizeSerializer, CustomTokenObtainPairSerializer
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

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # print("Datos de la solicitud:", request.data)
        try:
            # print("Datos de la solicitud:", request.data)  # Registra los datos de la solicitud
            response = super().post(request, *args, **kwargs)
            # print("Respuesta del super().post:", response.data)  # Registra la respuesta

            if response.status_code == 200:
                access_token = response.data.get("access")
                refresh_token = response.data.get("refresh")

                response.set_cookie(
                    "access",
                    access_token,
                    max_age=settings.AUTH_COOKIE_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE,
                )
                response.set_cookie(
                    "refresh",
                    refresh_token,
                    max_age=settings.AUTH_COOKIE_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE,
                )
            else:
                # print(f"Error en la respuesta: {response.data}")
                if response.status_code == status.HTTP_401_UNAUTHORIZED:
                    response.data = {
                        "error": "Por favor, verifica tu email y contraseña."
                    }
                elif response.status_code == status.HTTP_400_BAD_REQUEST:
                    response.data = {
                        "error": "Se produjo un error en la solicitud. Por favor, revisa los datos enviados."
                    }
            return response
            # return Response({"message": "SignIn exitoso."})
        except Exception as e:
            print(f"Excepción capturada: {e}")
            return Response(
                {
                    "error": "Ocurrió un error al autenticar el usuario, verifica tu informacion"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")

            response.set_cookie(
                "access",
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get("access")

        if access_token:
            request.data["token"] = access_token

        return super().post(request, *args, **kwargs)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.data["password"] != request.data["password_confirmation"]:
            return Response(
                {"error": "Las contraseñas no coinciden"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_serializer = UserCustomizeSerializer(
            data={
                "email": request.data["email"],
                "password": request.data["password"],
                # "role": [2],
            }  # aqui debo poner por defecto 3
        )
        #
        if user_serializer.is_valid():
            # print("we here")
            user = user_serializer.save()
            # print(user.id)
            profile_data = {
                "nombre": request.data["nombre"],
                "apellidoP": request.data["apellidoP"],
                "user": user.id,
            }
            profile_serializer = ProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(
                    {
                        "message": "Usuario creado con exito. Inicia sesión para continuar"
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # print(user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_serealizer = UserCustomizeSerializer(user)
        if user and user_serealizer:
            return Response(user_serealizer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Se genero un error al recuperar al usuario"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CheckUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, *args, **kwargs):
        auth = request.user
        # if hasattr(User, "rol") and isinstance(User.rol.field, models.ManyToManyField):
        #     user = User.objects.prefetch_related("rol").get(email=auth)
        # else:
        user = User.objects.get(email=auth)

        serializer = UserCustomizeSerializer(user)
        # print(user)
        if auth.is_authenticated:
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED
            )




class LogoutView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(
            "access",
            path="/",
            samesite="None",
        )
        response.delete_cookie(
            "refresh",
            path="/",
            samesite="None",
        )
        response.delete_cookie(
            "token",
            path="/",
            samesite="None",
        )
        return response
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         resp = Response({"detail": "logout ok"}, status=status.HTTP_200_OK)

#         # Variantes de borrado: sin domain y (si aplica) con domain
#         delete_variants = [
#             dict(path="/", secure=True, samesite="None"),
#         ]

#         # Si usas un domain explícito en algún lugar (no es tu caso por lo que pegaste),
#         # podrías añadir algo como:
#         # if getattr(settings, "SESSION_COOKIE_DOMAIN", None):
#         #     delete_variants.append(dict(path="/", secure=True, samesite="None",
#         #                                 domain=settings.SESSION_COOKIE_DOMAIN))

#         cookie_names = ["access", "refresh", "token", "__Host-access", "__Host-refresh"]

#         for opts in delete_variants:
#             for name in cookie_names:
#                 resp.delete_cookie(name, **opts)

#         return resp

# def user(request):
