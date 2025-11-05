from django.urls import path, include
from .views import RetriveTipoProducto
from rest_framework.routers import DefaultRouter
from invitaPro.views import EventosModelViewSet, ItinerarioModelViewSet

router = DefaultRouter()
router.register(r"eventos", EventosModelViewSet, basename="evento")
router.register(r"itinerarios", ItinerarioModelViewSet, basename="itinerario")

urlpatterns = [
    path('tipo-producto/all/', RetriveTipoProducto.as_view(), name="get"),
    # path()
    
    # eventos
    
    path('invitapro/', include(router.urls))
]