from django.urls import path, include
from .views import StudentUpdateProfile, CursoView, CursoPaginatedView, CursoPanelView, CuntCursos, CursosEstudianteModelViewSet
from rest_framework.routers import DefaultRouter
from .views import ComentarioViewSet, EnlaceViewSet, PlataformaViewSet

router = DefaultRouter()
router.register(r"comentarios", ComentarioViewSet, basename="comentario")
router.register(r"enlaces", EnlaceViewSet, basename="enlace")
router.register(r"plataformas-imparticion", PlataformaViewSet, basename="plataforma-imparticion")
router.register(r"cursos", CursosEstudianteModelViewSet, basename="curso")

urlpatterns = [
    path("student/cursos/", CursoView.as_view(), name="get"),
    path("student/cursos/all/", CursoPaginatedView.as_view(), name="get"),
    path("student/total-programs/", CuntCursos.as_view(), name="get"),
    path("student/cursos/<int:id>/", CursoPanelView.as_view()),
    path("student/profile/", StudentUpdateProfile.as_view(), name="get"),
    path("student/update/profile/", StudentUpdateProfile.as_view(), name="patch"),
    
    # Comunidad e interaccion
    path("plataforma/", include(router.urls))
]