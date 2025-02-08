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
        if data['revisions'] < -1:
            raise serializers.ValidationError("Die Anzahl der Überarbeitungen muss -1 oder größer sein.")
        if data['delivery_time_in_days'] <= 0:
            raise serializers.ValidationError("Die Lieferzeit muss positiv sein.")
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
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        for detail_dict in details_data:
            OfferDetail.objects.create(offer=offer, **detail_dict)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if details_data is not None:
            instance.details.all().delete()
            for detail_dict in details_data:
                OfferDetail.objects.create(offer=instance, **detail_dict)
        
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        action = self.context.get('action', '')

        if action == 'create':
            rep.pop('min_price', None)
            rep.pop('min_delivery_time', None)
            rep.pop('user_details', None)
            rep.pop('created_at', None)
            rep.pop('updated_at', None)
            rep.pop('user', None)

        elif action == 'list':
            rep['details'] = [
                {'id': d['id'], 'url': f"/offerdetails/{d['id']}/"}
                for d in rep.get('details', [])
            ]

        elif action == 'retrieve':
            rep.pop('min_price', None)
            rep.pop('min_delivery_time', None)
            rep.pop('user_details', None)
        return rep


class FileUploadSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = FileUpload
        fields = ['path']

    def create(self, validated_data):
        return FileUpload.objects.create(**validated_data)

    def get_path(self, obj):
        if obj.image:
            return obj.image.url
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
    file = serializers.SerializerMethodField() 

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'first_name',
            'last_name',
            'file', 
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
        if obj.file and obj.file.image:  
            return obj.file.image.url  
        return None 



class BusinessProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Profile 
        fields = [
            'user',        
            'file',        
            'location',    
            'tel',         
            'description', 
            'working_hours', 
            'type',        
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer() 

    class Meta:
        model = Profile
        fields = [
            'user',       
            'file',        
            'uploaded_at', 
            'type',        
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
        read_only_fields = ['reviewer']
    
    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            reviewer = request.user
            business_user = data.get('business_user')

            if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
                raise serializers.ValidationError("Du hast diesen Benutzer bereits bewertet.")
        return data