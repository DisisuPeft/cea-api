from django.urls import path, re_path
from .views.modulos import Modulosview, TabsView, PestaniaEstudianteView
from .views import ManageUsersview, ManageUserAccessView

urlpatterns = [
    # re_path(
    #     r'^o/(?P<provider>\S+)/$',
    #     CustomProviderAuthView.as_view(),
    #     name='provider-auth'
    # ),
    path("menu/all/", Modulosview.as_view(), name="get"),
    path("tabs/all/<int:id>", TabsView.as_view(), name="get"),
    path("plataforma/pestanias/", PestaniaEstudianteView.as_view(), name="get"),

    path("plataforma/retrieve-users/", ManageUsersview.as_view(), name="get"),
    
    
    # accesos a tabs y modulos
    path("plataforma/add-access/", ManageUserAccessView.as_view(), name="post"),
    
    # usuarios
    path("plataforma/users/create", ManageUsersview.as_view(), name="post")
]
