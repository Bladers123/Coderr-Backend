from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from ..models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend




class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.prefetch_related('details').all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # pagination_class = None

    # filterset_fields = ['creator_id', 'price', 'created_at']
    # search_fields = ['min_price', 'created_at']
    # ordering_fields = ['min_price', 'created_at']


    def perform_create(self, serializer):
        # Setzt den angemeldeten Benutzer als den Benutzer des Angebots
        serializer.save(user=self.request.user)



class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.select_related('offer').all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]

