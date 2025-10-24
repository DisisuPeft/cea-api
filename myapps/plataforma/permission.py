from rest_framework.permissions import BasePermission, SAFE_METHODS

class EsAutorORolPermitido(BasePermission):
    def __init__(self, roles_permitidos=None):
        self.roles_permitidos = roles_permitidos or ["Administrador"]
        
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        is_autor = obj.usuario_id == user.id
        has_role = user.roleID.filter(name__in=self.roles_permitidos).exists()
        return is_autor or has_role
    
def EsAutorORolPermitidoConRoles(roles_permitidos):
    class CustomPermission(EsAutorORolPermitido):
        def __init__(self):
            super().__init__(roles_permitidos)
    return CustomPermission