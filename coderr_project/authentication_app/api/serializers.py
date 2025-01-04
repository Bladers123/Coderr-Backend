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
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'type')


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