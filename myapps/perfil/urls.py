from django.urls import path, re_path
from .views import (
    ProfileOpt,
)



urlpatterns = [

    path('users/myprofile/', ProfileOpt.as_view(), name="get"),
    path('users/myprofile/edit/', ProfileOpt.as_view(), name="patch"),
    # path('admin/usuarios/editar/', UsuariosAdministrador.as_view(), name="patch"),
    # path('admin/usuarios/crear/', UsuariosAdministrador.as_view(), name="post"),
    # path('auth/refresh/', CustomTokenRefreshView.as_view()),
    # path('auth/verify/', CustomTokenVerifyView.as_view()),
    # path('auth/register/', RegisterView.as_view()),
    # path('logout/', LogoutView.as_view()),


    # path('auth/user/', ProfileView.as_view()),
    # path('check/user/', CheckUser.as_view()),
]