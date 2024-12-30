from rest_framework import serializers
from ..models import Offer, OfferDetail
from django.contrib.auth.models import User
from ..models import FileUpload


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def validate(self, data):
        # Validierung der `revisions`
        if data['revisions'] < -1:
            raise serializers.ValidationError("Die Anzahl der Überarbeitungen muss -1 oder größer sein.")
        # Validierung der `delivery_time_in_days`
        if data['delivery_time_in_days'] <= 0:
            raise serializers.ValidationError("Die Lieferzeit muss positiv sein.")
        # Validierung der Features
        if not data['features']:
            raise serializers.ValidationError("Es muss mindestens ein Feature angegeben werden.")
        return data


class OfferWriteSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        # Hier ggf. Felder definieren, die du beim POST/PUT/PATCH
        # bearbeiten können möchtest:
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate(self, data):
        # Deine bereits vorhandenen Validierungen (z. B. Anzahl Details, offer_types usw.)
        if len(data['details']) != 3:
            raise serializers.ValidationError("Es müssen genau drei Angebotsdetails angegeben werden.")
        offer_types = [detail['offer_type'] for detail in data['details']]
        if sorted(offer_types) != ['basic', 'premium', 'standard']:
            raise serializers.ValidationError("Es müssen die Typen 'basic', 'standard' und 'premium' enthalten sein.")
        return data

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    
class OfferReadSerializer(serializers.ModelSerializer):
    """Nur Felder fürs Anzeigen (GET)"""
    details = OfferDetailSerializer(many=True, read_only=True)
    user_details = UserDetailSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['file', 'uploaded_at']