from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from ..models import Offer, OfferDetail
from .serializers import OfferWriteSerializer, OfferDetailSerializer, FileUploadSerializer, OfferReadSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import FileUpload
from rest_framework.views import APIView
from rest_framework import status



class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferReadSerializer

    def list(self, request, *args, **kwargs):
        """
        Gibt alle Angebote mit dem gewünschten Listen-Format zurück.
        """
        queryset = self.get_queryset()
        serializer = OfferReadSerializer(queryset, many=True)
        data = []

        for offer in serializer.data:
            details = [
                {"id": detail["id"], "url": f"/offerdetails/{detail['id']}/"}
                for detail in offer["details"]
            ]
            data.append({
                **offer,
                "details": details  # Details auf das Kurzformat anpassen
            })

        return Response(data)

    def create(self, request, *args, **kwargs):
        """
        Behandelt die Erstellung eines neuen Angebots und gibt das gewünschte Format zurück.
        """
        serializer = OfferWriteSerializer(data=request.data)
        if serializer.is_valid():
            offer = serializer.save()
            details = OfferDetailSerializer(offer.details.all(), many=True).data
            response_data = {
                "id": offer.id,
                "title": offer.title,
                "image": offer.image.url if offer.image else None,
                "description": offer.description,
                "details": details
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Gibt ein einzelnes Angebot mit allen Details und User-Informationen zurück.
        """
        instance = self.get_object()
        serializer = OfferReadSerializer(instance)
        offer_data = serializer.data

        # Details im Vollformat übernehmen
        details = OfferDetailSerializer(instance.details.all(), many=True).data

        response_data = {
            **offer_data,
            "details": details,  # Vollständige Details
        }
        return Response(response_data)




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
        