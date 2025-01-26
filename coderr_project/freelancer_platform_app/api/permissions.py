from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    """
    Erlaubt den Zugriff nur für Benutzer mit dem Typ 'customer'.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.type == 'customer'


class IsBusiness(BasePermission):
    """
    Erlaubt den Zugriff nur für Benutzer mit dem Typ 'business'.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.type == 'business'
    
    
class IsOwnerOrAdmin(BasePermission):
    """
    Erlaubt Änderungen oder Löschungen nur für den Ersteller der Bewertung oder Admins.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reviewer or request.user.is_staff
