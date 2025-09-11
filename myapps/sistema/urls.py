from django.urls import path, re_path
from .views.modulos import Modulosview, TabsView, PestaniaEstudianteView, AssignTabsView
from .views import ManageUsersview, ManageUserAccessView, ManageEditUserView

urlpatterns = [
    # re_path(
    #     r'^o/(?P<provider>\S+)/$',
    #     CustomProviderAuthView.as_view(),
    #     name='provider-auth'
    # ),
    path("menu/all/", Modulosview.as_view(), name="get"),
    path("tabs/all/", TabsView.as_view(), name="get"),
    path("plataforma/pestanias/", PestaniaEstudianteView.as_view(), name="get"),

    # Manage users plataforma
    path("plataforma/users/update/", ManageEditUserView.as_view(), name="patch"),
    path("plataforma/retrieve-users/", ManageUsersview.as_view(), name="get"),
    path("plataforma/users/create/", ManageUsersview.as_view(), name="post"),
    path("plataform/edit-users/<int:id>/", ManageEditUserView.as_view(), name="get"),
    
    # accesos a tabs y modulos
    path('plataforma/retrive-submodules/<int:id>', AssignTabsView.as_view(), name="get"),
    path("plataforma/add-access/", ManageUserAccessView.as_view(), name="post"),
    path("plataform/edit-users/<int:id>", ManageEditUserView.as_view(), name="get"),
]
