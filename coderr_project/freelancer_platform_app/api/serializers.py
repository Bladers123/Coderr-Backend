from rest_framework import serializers
from ..models import Offer, OfferDetail
from django.contrib.auth.models import User

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'offer', 'url']


class OfferSerializer(serializers.ModelSerializer):
    # Nutzt den OfferDetailSerializer, um die Details als verschachtelte Daten anzuzeigen
    details = OfferDetailSerializer(many=True, read_only=True)
    user_details = UserDetailSerializer(source='user', read_only=True)  # Hole die Daten direkt vom Benutzer


    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'description', 'min_price', 'min_delivery_time', 'details', 'user_details']
