from django.urls import path, include
from .views import StudentUpdateProfile, CursoView, CursoPaginatedView, CursoPanelView, CuntCursos
from rest_framework.routers import DefaultRouter
from .views import ComentarioViewSet

router = DefaultRouter()
router.register(r"comentarios", ComentarioViewSet, basename="comentario")

urlpatterns = [
    # path("student/create/", StudentsView.as_view(), name="post"),
    # path("students/all/", StudentsView.as_view(), name="get"),
    path("student/cursos/", CursoView.as_view(), name="get"),
    path("student/cursos/all/", CursoPaginatedView.as_view(), name="get"),
    path("student/total-programs/", CuntCursos.as_view(), name="get"),
    path("student/cursos/<int:id>/", CursoPanelView.as_view()),
    path("student/profile/", StudentUpdateProfile.as_view(), name="get"),
    path("student/update/profile/", StudentUpdateProfile.as_view(), name="patch"),
    
    # Comunidad e interaccion
    path("plataforma/", include(router.urls))
]