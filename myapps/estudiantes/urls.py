from django.urls import path, re_path
from .views import (
    StudentsView, StudentView, StudentUpdateView
)

urlpatterns = [
    path("student/create/", StudentsView.as_view(), name="post"),
    path("students/all/", StudentsView.as_view(), name="get"),
    path("student/<int:id>/", StudentView.as_view(), name="get"),
    path("student/edit/<int:id>/", StudentUpdateView.as_view(), name="get"),
    path("student/update/<int:id>/", StudentUpdateView.as_view(), name="patch")
]
