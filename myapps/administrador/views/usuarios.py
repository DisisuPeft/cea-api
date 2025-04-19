from django.shortcuts import render
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
# from myapps.perfil.models import Profile
from myapps.perfil.serializer import ProfileSerializer
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.authentication.models import Roles, Permissions
from myapps.authentication.serializers import RoleCustomizeSerializer, PermissionCustomizeSerializer

class UsuariosAdministrador(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"error": "El usuario no se encuentra autenticado"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
        usuarios = UserCustomize.objects.exclude(email=user.email)
    
        if not usuarios.exists():
            return Response(
                "No existen usuarios", 
                status=status.HTTP_404_NOT_FOUND
            )
    
        serializer = UserCustomizeSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
    
    def post(self, request, *args, **kwargs):
        # print(request.data)
        role = [int(roles) for roles in request.data['role']]
        user_dict = {}
        perfil_dict = {}
        user_headers = ['email', 'password']
        perfil_headers = [
            "nombre", "apellidoP", "apellidoM", "edad", 
            "fechaNacimiento", "genero", "nivEdu", "telefono"
        ]

        for i in user_headers:
            if i in request.data and request.data[i]:
                user_dict[i] = request.data[i]
        user_dict['role'] = role
        user_serializer = UserCustomizeSerializer(data=user_dict)
        
        if user_serializer.is_valid():
            user_instance = user_serializer.save()
            for p in perfil_headers:
                if p in request.data and request.data[p]:
                    perfil_dict[p] = request.data[p]
            perfil_dict['user'] = user_instance.id
            # perfil_data = {
            #     'nombre': request.data['nombre'],
            #     'apellidoP': request.data['apellidoP'],
            #     'apellidoM': request.data['apellidoM'], 
            #     'edad': request.data['edad'], 
            #     'fechaNacimiento': request.data['fechaNacimiento'], 
            #     'genero': request.data['genero'], 
            #     'nivEdu': request.data['nivEdu'], 
            #     'telefono':request.data['telefono'],
            #     'user': user_instance.id,
            # }
            # print(user_instance.id)
            perfil_serializer = ProfileSerializer(data=perfil_dict)
            if perfil_serializer.is_valid():
                perfil_serializer.save()
                return Response({"message": "Usuario creado con exito"}, status=status.HTTP_201_CREATED)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        

class EditUsersAdministrador(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, id):
        user = UserCustomize.objects.get(id=id)
        if not user:
            return Response(u"User not found", status=status.HTTP_400_BAD_REQUEST)  
        serializer = UserCustomizeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user_id = request.data['id']  
        # print(request.data)
        try:
            user = UserCustomize.objects.get(id=user_id)
            profile = user.profile
            # print(user, profile)
        except UserCustomize.DoesNotExist:
            return Response("Usuario no encontrado", status=status.HTTP_404_NOT_FOUND)

        profile_data = {}
        if 'email' in request.data and request.data['email']:
            user.email = request.data['email']

        if 'roleID' in request.data and request.data['roleID']:
            roles = request.data['roleID']
            # print(roles)
            user.roleID.clear()
            for rol in roles:
                # print(rol)
                user.roleID.add(rol['id'])
        
        user.save()
        profile_req = request.data['profile']
        # print(profile_req)
        for key, value in profile_req.items():
            if key in profile_req and profile_req[key]:
                if value:
                    profile_data[key] = profile_req[key]
        print(profile_data)
        profile_serializer = ProfileSerializer(
            profile, 
            data=profile_data, 
            partial=True  
        )   
        try:
            if profile_data:
                if profile_serializer.is_valid():
                    profile_serializer.save()
                    return Response("Usuario editado con exito", status=status.HTTP_200_OK)
                else:
                    return Response(profile_serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            
        # return Response("Hola", status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)         

class RolesView(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        roles = Roles.objects.all()
        
        if not roles: 
            return Response("Roles not found", status=status.HTTP_400_BAD_REQUEST)  
        serializer = RoleCustomizeSerializer(roles, many=True)
        # sinroles = serializer.data
        # print(sinroles.pop('permission'))
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PermissionView(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        permissions = Permissions.objects.all()
        
        if not permissions: 
            return Response("Roles not found", status=status.HTTP_400_BAD_REQUEST)  
        serializer = PermissionCustomizeSerializer(permissions, many=True)
        # sinroles = serializer.data
        # print(sinroles.pop('permission'))
        return Response(serializer.data, status=status.HTTP_200_OK)