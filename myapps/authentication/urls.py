from django.urls import path, re_path
from .views import (
    # CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
    RegisterView,
    ProfileView,
    CheckUser,
)

urlpatterns = [
    # re_path(
    #     r'^o/(?P<provider>\S+)/$',
    #     CustomProviderAuthView.as_view(),
    #     name='provider-auth'
    # ),
    path("auth/login/", CustomTokenObtainPairView.as_view()),
    path("auth/refresh/", CustomTokenRefreshView.as_view()),
    path("auth/verify/", CustomTokenVerifyView.as_view()),
    path("auth/register/", RegisterView.as_view()),
    path("logout/", LogoutView.as_view()),
    # path('auth/user/', ProfileView.as_view()),
    path("auth/user/", CheckUser.as_view()),
]
