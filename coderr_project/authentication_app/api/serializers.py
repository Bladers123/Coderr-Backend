from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework import status
from ..models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            field.name
            for field in CustomUser._meta.get_fields()
            if not field.is_relation or field.one_to_one or field.many_to_one
        ]  # Nur konkrete Felder (keine umgekehrten Relationen)




class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)  # Nicht in der DB, nur für die Eingabe

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'repeated_password', 'type')

    def validate(self, data):
        password = data.get('password')
        repeated_password = data.get('repeated_password')
        email = data.get('email')
        username = data.get('username')

        if password != repeated_password:
            raise serializers.ValidationError({
                'repeated_password': 'Passwörter stimmen nicht überein.'
            })
        
        if len(password) < 8:
            raise serializers.ValidationError({
                'password': 'Passwort muss mindestens 8 Zeichen lang sein.'
            })

        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({
                'email': 'Diese E-Mail-Adresse ist bereits registriert.'
            })
        
        if username and CustomUser.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError({
                'username': 'Dieser Nutzername ist bereits registriert.'
            })

        if not all([password, repeated_password, email, username]):
            raise serializers.ValidationError("Ungültige Eingaben. Bitte alle erforderlichen Felder ausfüllen.")

        return data

    def create(self, validated_data):
        # Entferne `repeated_password`, da es nicht im Model existiert
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            type=validated_data['type']
        )
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attributes):
        username = attributes.get('username')
        password = attributes.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Falsche Anmeldeinformationen oder ungültige Eingabe.', status.HTTP_400_BAD_REQUEST)

        attributes['user'] = user
        return attributes