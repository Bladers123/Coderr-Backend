from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(f"Benutzer: {request.user}")
        print(f"Objekt-Besitzer: {obj.user}")
        print(f"Angeforderte Methode: {request.method}")
        print(f"Ist Besitzer: {obj.user == request.user}")
        # Prüfe SAFE_METHODS oder Besitzerstatus
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
