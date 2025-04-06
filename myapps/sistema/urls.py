from django.urls import path, re_path
from .views import (
    # CustomProviderAuthView,
    Modulosview, TabsView
)

urlpatterns = [
    # re_path(
    #     r'^o/(?P<provider>\S+)/$',
    #     CustomProviderAuthView.as_view(),
    #     name='provider-auth'
    # ),
    path("menu/all/", Modulosview.as_view(), name="get"),
    path("tabs/all/", TabsView.as_view(), name="get")
    # path("auth/refresh/", CustomTokenRefreshView.as_view()),
    # path("auth/verify/", CustomTokenVerifyView.as_view()),
    # path("auth/register/", RegisterView.as_view()),
    # path("logout/", LogoutView.as_view()),
    # # path('auth/user/', ProfileView.as_view()),
    # path("auth/user/", CheckUser.as_view()),
]
