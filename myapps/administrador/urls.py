from django.urls import path, re_path
from .views.usuarios import UsuariosAdministrador, EditUsersAdministrador, RolesView



urlpatterns = [
    #EL detalle es que esta usando la ruta get de todos los usuarios, revisar eso
    path('cea/usuarios/', UsuariosAdministrador.as_view(), name="get"),
    path('cea/usuarios/crear/', UsuariosAdministrador.as_view(), name="post"),
    path('cea/usuario/<int:id>', EditUsersAdministrador.as_view(), name="get"),
    path('cea/usuarios/update/', EditUsersAdministrador.as_view(), name="patch"),
    # path('auth/refresh/', CustomTokenRefreshView.as_view()),
    # path('auth/verify/', CustomTokenVerifyView.as_view()),
    # path('auth/register/', RegisterView.as_view()),
    # path('logout/', LogoutView.as_view()),
    path('cea/roles/', RolesView.as_view(), name="get"),

    # path('auth/user/', ProfileView.as_view()),
    # path('check/user/', CheckUser.as_view()),
]