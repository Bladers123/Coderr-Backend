from django_filters import rest_framework as filters
from ..models import Offer

class OfferFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gte')  # Mindestpreis
    min_delivery_time = filters.NumberFilter(field_name='min_delivery_time', lookup_expr='gte')  # minimale Lieferzeit
    creator_id = filters.NumberFilter(field_name='user__id', lookup_expr='exact')  # Benutzer-ID (indirekt über user)

    class Meta:
        model = Offer
        fields = ['user', 'min_price', 'min_delivery_time']  # Existierende Felder im Modell
