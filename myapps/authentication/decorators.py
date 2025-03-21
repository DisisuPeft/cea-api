from functools import wraps

from rest_framework import status
from rest_framework.response import Response
from myapps.authentication.models import Roles


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            # Verificar si el usuario tiene algún rol permitido
            if user.is_authenticated and user.roleID.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)

            # Si no tiene el rol, denegar acceso
            return Response({"error": "No tienes permiso para acceder a este recurso"}, status=status.HTTP_403_FORBIDDEN)

        return _wrapped_view

    return decorator