from django.urls import path, re_path
from .views import (
    GetProgramasCatalogView,
    GetCiclosView
)



urlpatterns = [
    # Ciclos
    path('control-escolar/ciclos/all/', GetCiclosView.as_view(), name="get"),
    path('control-escolar/ciclos/create/', GetCiclosView.as_view(), name="post"),
    
    # Programas educativos
    path('control-escolar/programas-educativos/', GetProgramasCatalogView.as_view(), name="get"),

]