from django.urls import path, include
from .views import (
    GetProgramasCatalogView,
    GetCiclosView,
    RetrieveCiclosParamView,
    ObtainCiclosParamView,
    GetProgramsRequestView,
    GetProgramasView,
    GetProgramLandingView,
    GetProgramaView,
    ProgramaViewSet,
    TipoProgramaViewSet,
    InscripcionModelViewSet,
    TipoPagoViewSet,
    PagosModelViewSet,
    GetProgramasEstudianteView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"programas", ProgramaViewSet, basename="programa")
router.register(r"tipos-programas", TipoProgramaViewSet, basename="tipo-programa")
router.register(r"inscripciones", InscripcionModelViewSet, basename="inscripcion")
router.register(r"tipos-pagos", TipoPagoViewSet, basename="tipo-pago")
router.register(r"pagos", PagosModelViewSet, basename="pago")

urlpatterns = [
    # Ciclos
    path('control-escolar/ciclos/all/', GetCiclosView.as_view(), name="get"),
    path('control-escolar/ciclos/create/', GetCiclosView.as_view(), name="post"),
    path('control-escolar/ciclos-query/', RetrieveCiclosParamView.as_view(), name="get"),
    path('control-escolar/ciclo/', ObtainCiclosParamView.as_view(), name="get"),
    # Programas educativos
    path('control-escolar/programas-educativos/', GetProgramasCatalogView.as_view(), name="get"),
    path('control-escolar/oferta-educativa/', GetProgramLandingView.as_view(), name="get"),
    # crm
    path('control-escolar/cat/programas/', GetProgramsRequestView.as_view(), name="get"),
    path('control-escolar/programa/<int:id>/', GetProgramaView.as_view(), name="get"),
    
    path('control-escolar/programas/todos/', GetProgramasView.as_view(), name="get"),
    path('control-escolar/programas/oferta/', GetProgramasEstudianteView.as_view(), name="get"),
    # path('catalo')
    path("control-escolar/", include(router.urls))
]