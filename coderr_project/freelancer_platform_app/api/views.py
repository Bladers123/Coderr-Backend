from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from ..models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer, FileUploadSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import FileUpload
from rest_framework.views import APIView
from rest_framework import status




class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context



class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.select_related('offer').all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]




class FileUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        