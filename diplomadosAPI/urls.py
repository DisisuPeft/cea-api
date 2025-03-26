"""
URL configuration for diplomadosAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapps.authentication import views as auth_views
from myapps.perfil import views as perfil_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('register', auth_views.register, name='register'),
    path('api/', include('myapps.authentication.urls')),
    path('api/', include('myapps.administrador.urls')),
    path('api/', include('myapps.perfil.urls')),
    path('api/', include('myapps.cursos.urls')),
    path('api/', include('myapps.configuracion.urls')),
    path('api/', include('myapps.centro_educativo.urls'))
    # path('perfil', perfil_views.getprofile, name='perfil'),
]
