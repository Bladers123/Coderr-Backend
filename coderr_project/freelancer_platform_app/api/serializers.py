from rest_framework import serializers
from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'offer', 'url']


class OfferSerializer(serializers.ModelSerializer):
    # Nutzt den OfferDetailSerializer, um die Details als verschachtelte Daten anzuzeigen
    details = OfferDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'description', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'details',]
        read_only_fields = ['user', 'created_at', 'updated_at']


