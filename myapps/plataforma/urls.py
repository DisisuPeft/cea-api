from django.urls import path, re_path
from .views import StudentUpdateProfile, CursoView, CursoPaginatedView, CursoPanelView

urlpatterns = [
    # path("student/create/", StudentsView.as_view(), name="post"),
    # path("students/all/", StudentsView.as_view(), name="get"),
    path("student/cursos/", CursoView.as_view(), name="get"),
    path("student/cursos/all/", CursoPaginatedView.as_view(), name="get"),
    path("student/cursos/<int:id>/", CursoPanelView.as_view()),
    path("student/profile/<int:id>/", StudentUpdateProfile.as_view(), name="get"),
    path("student/update/profile/<int:id>/", StudentUpdateProfile.as_view(), name="patch")
]