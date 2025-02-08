from django_filters import rest_framework as filters
from ..models import Offer, Review
import django_filters
from rest_framework.filters import OrderingFilter



class OfferFilter(filters.FilterSet):
    creator_id = filters.NumberFilter(field_name='user__id', lookup_expr='exact') 
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_delivery_time = filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte') 
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']



class Updated_atOrderingFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        ordering = request.query_params.get(self.ordering_param)
        if ordering == 'updated_at':
            return ['-updated_at']
        elif ordering == '-updated_at':
            return ['updated_at']
        return super().get_ordering(request, queryset, view)




class ReviewFilter(django_filters.FilterSet):
    business_user_id = django_filters.NumberFilter(field_name="business_user_id", lookup_expr="exact")
    reviewer_id = django_filters.NumberFilter(field_name="reviewer_id", lookup_expr="exact")

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']

