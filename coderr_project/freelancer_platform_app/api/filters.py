from django_filters import rest_framework as filters
from ..models import Offer




class OfferFilter(filters.FilterSet):
    creator_id = filters.NumberFilter(field_name='user__id', lookup_expr='exact')  # Benutzer-ID (indirekt über user)
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gte')  # Mindestpreis
    max_delivery_time = filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte')  # minimale Lieferzeit
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')  # Sucht nach dem Titel

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']  # Existierende Felder im Modell
