from django.urls import path, include
from .views import NivelesEducativosView, GeneroView, EstadosRepublicaView, MunicipioView, EspecialidadView, EstatusView, InstitutosModelViewSet, MetodoPagoModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'institutos', InstitutosModelViewSet, basename="instituto")
router.register(r'metodos-pago', MetodoPagoModelViewSet, basename="metodo-pago")

urlpatterns = [

    path('catalogos/niveles-educativos/', NivelesEducativosView.as_view(), name="get"),
    path('catalogos/generos/', GeneroView.as_view(), name="get"),
    path('catalogos/estados-republica/', EstadosRepublicaView.as_view(), name="get"),
    path('catalogos/entidad/municipios/<int:id>', MunicipioView.as_view(), name="get"),
    path('catalagos/especialidades/all/', EspecialidadView.as_view(), name="get"),
    path('catalagos/maestro/status/all/', EstatusView.as_view(), name="get"),

    path('catalagos/', include(router.urls))
]