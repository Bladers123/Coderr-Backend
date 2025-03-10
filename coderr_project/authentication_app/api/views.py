from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from .serializers import CustomUserSerializer, RegistrationSerializer, LoginSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from ..models import CustomUser



class UserViewSet(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

class RegistrationViewSet(CreateModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': 'Erfolgreiche Registrierung',
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': 'Erfolgreiche Anmeldung',
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            },
            status=status.HTTP_200_OK
        )