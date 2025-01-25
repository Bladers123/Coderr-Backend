from rest_framework import serializers
from ..models import Offer, OfferDetail, Order, Profile, Review
from authentication_app.models import CustomUser
from ..models import FileUpload
from ..models import models

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['pk', 'first_name', 'last_name', 'username']

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


class OfferSerializer(serializers.ModelSerializer):
    user_details = UserDetailSerializer(source='user', read_only=True)    
    details = OfferDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at',
            'updated_at', 'min_price', 'min_delivery_time', 'details', 'user_details'
        ]

    def get_min_price(self, obj):
        min_price = obj.details.aggregate(models.Min('price'))['price__min']
        return min_price if min_price is not None else 0.00

    def get_min_delivery_time(self, obj):
        min_delivery_time = obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min']
        return min_delivery_time if min_delivery_time is not None else 0


    def create(self, validated_data):
        # Hier holen wir uns die "details"-Liste aus den validierten Daten
        details_data = validated_data.pop('details', [])
        # Erstellen das Offer
        offer = Offer.objects.create(**validated_data)
        # Erstellen die OfferDetail-Einträge
        for detail_dict in details_data:
            OfferDetail.objects.create(offer=offer, **detail_dict)
        return offer

    def update(self, instance, validated_data):
        # Falls du Updates an den Details erlauben willst, 
        # müsstest du hier eine Logik implementieren.
        details_data = validated_data.pop('details', None)
        
        # Erst die restlichen Felder vom Offer updaten
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if details_data is not None:
            # Beispiel: Alte Details löschen und neue erstellen
            instance.details.all().delete()
            for detail_dict in details_data:
                OfferDetail.objects.create(offer=instance, **detail_dict)
        
        return instance

    def to_representation(self, instance):
        """
        Du kannst hier (optional) unterscheiden, ob du im 'list' oder 'retrieve'
        bist, und die Ausgabe von `details` anpassen (Kurzinfo oder Vollformat).
        """
        rep = super().to_representation(instance)
        action = self.context.get('action', '')

        # get nach dem post
        if action == 'create':
            rep.pop('min_price', None)
            rep.pop('min_delivery_time', None)
            rep.pop('user_details', None)
            rep.pop('created_at', None)
            rep.pop('updated_at', None)
            rep.pop('user', None)

        
        # get von der liste
        elif action == 'list':
            # Kurzformat => Nur ID + URL
            rep['details'] = [
                {'id': d['id'], 'url': f"/offerdetails/{d['id']}/"}
                for d in rep.get('details', [])
            ]

        # get von einem einzelnen objekt
        elif action == 'retrieve':
            rep.pop('min_price', None)
            rep.pop('min_delivery_time', None)
            rep.pop('user_details', None)
        return rep




class FileUploadSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()  # Neues Feld für den Bildpfad

    class Meta:
        model = FileUpload
        fields = ['path']

    def create(self, validated_data):
        # Datei speichern
        return FileUpload.objects.create(**validated_data)

    def get_path(self, obj):
        # Gib den relativen Pfad zur Datei zurück
        if obj.image:
            return obj.image.url  # z. B. "/media/uploads/example.pdf"
        return None



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']




class OrderCountSerializer(serializers.Serializer):
    order_count = serializers.IntegerField()


class CompletedOrderCountSerializer(serializers.Serializer):
    completed_order_count = serializers.IntegerField()


class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()



class ProfileSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='user.type', read_only=True)
    file = serializers.SerializerMethodField()  # Neues Feld für den Pfad

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'first_name',
            'last_name',
            'file',  # Hier wird jetzt nur der Pfad als String zurückgegeben
            'location',
            'tel',
            'description',
            'working_hours',
            'email',
            'created_at',
            'type',
        ]

    def get_file(self, obj):
        """
        Gibt den Pfad der Datei zurück, oder None, wenn keine Datei vorhanden ist.
        """
        if obj.file and obj.file.image:  # Sicherstellen, dass eine Datei existiert
            return obj.file.image.url  # Rückgabe des relativen Pfads (z. B. "/media/uploads/example.pdf")
        return None  # Kein Bild hochgeladen



class BusinessProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()  # Verschachtelter Serializer für Benutzer

    class Meta:
        model = Profile  # Verwende das Profile-Modell
        fields = [
            'user',        # Verschachtelte Benutzerdaten
            'file',        # Profilbild
            'location',    # Standort
            'tel',         # Telefonnummer
            'description', # Beschreibung
            'working_hours', # Arbeitszeiten
            'type',        # Profiltyp (business/customer)
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()  # Verschachtelter Serializer für Benutzer

    class Meta:
        model = Profile
        fields = [
            'user',        # Benutzerinformationen
            'file',        # Profilbild
            'uploaded_at', # Hochladezeit
            'type',        # Profiltyp (customer)
        ]



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]