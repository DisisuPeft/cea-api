from django.urls import path, re_path
from .views import (
    NivelesEducativos,
)



urlpatterns = [

    path('cea/niveles-educativos/', NivelesEducativos.as_view(), name="get"),
    # path('cea/usuarios/editar/', UsuariosAdministrador.as_view(), name="patch"),
    # path('cea/usuarios/crear/', UsuariosAdministrador.as_view(), name="post"),
    # path('auth/refresh/', CustomTokenRefreshView.as_view()),
    # path('auth/verify/', CustomTokenVerifyView.as_view()),
    # path('auth/register/', RegisterView.as_view()),
    # path('logout/', LogoutView.as_view()),
    

    # path('auth/user/', ProfileView.as_view()),
    # path('check/user/', CheckUser.as_view()),
]