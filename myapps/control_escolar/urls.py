from django.urls import path, re_path
from .views import (
    GetProgramasCatalogView,
    GetCiclosView,
    RetrieveCiclosParamView,
    ObtainCiclosParamView,
    GetProgramsRequestView
)



urlpatterns = [
    # Ciclos
    path('control-escolar/ciclos/all/', GetCiclosView.as_view(), name="get"),
    path('control-escolar/ciclos/create/', GetCiclosView.as_view(), name="post"),
    path('control-escolar/ciclos-query/', RetrieveCiclosParamView.as_view(), name="get"),
    path('control-escolar/ciclo/', ObtainCiclosParamView.as_view(), name="get"),
    # Programas educativos
    path('control-escolar/programas-educativos/', GetProgramasCatalogView.as_view(), name="get"),
    # crm
    path('control-escolar/cat/programas/', GetProgramsRequestView.as_view(), name="get"),
    # path('catalo')

]