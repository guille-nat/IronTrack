from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    permit access only owner of the objet or admins
    """

    def has_object_permission(self, request, view, obj):
        # Permitir a los administradores acceder a todos los objetos
        if request.user.is_superuser:
            return True
        # Verificar si el objeto pertenece al usuario autenticado
        return obj.user == request.user


class IsOwner(BasePermission):
    """
    permit access only if the authentication user is owner of the object
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
