from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from ..models import Offer, OfferDetail, Order, OrderCount
from .serializers import CompletedOrderCountSerializer, OfferSerializer, OfferDetailSerializer, FileUploadSerializer, OrderCountSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import FileUpload
from rest_framework.views import APIView
from rest_framework import status
from .filters import OfferFilter
from django.contrib.auth import get_user_model
from django.views.generic.detail import DetailView
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound



User = get_user_model()


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # Hier geben wir ein leeres Objekt zurück und ändern den Statuscode
        return Response({}, status=status.HTTP_200_OK)



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
        




class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # Hier geben wir ein leeres Objekt zurück und ändern den Statuscode
        return Response({}, status=status.HTTP_200_OK)
    






class OrderCountView(APIView):
    def get(self, request, pk):
        # Berechne die Anzahl der Orders für den gegebenen business_user
        order_count = Order.objects.filter(business_user=pk).count()

        if order_count == 0:
            raise NotFound({"error": f"Business user not found"})

        # Erstelle die Daten
        data = {
            "order_count": order_count
        }

        # Nutze den Serializer zur Validierung und Ausgabe
        serializer = OrderCountSerializer(data)
        return Response(serializer.data)





class CompletedOrderCountView(APIView):
    def get(self, request, pk):
        # Zähle nur Orders mit Status 'completed' für den gegebenen business_user
        completed_order_count = Order.objects.filter(business_user=pk, status='completed').count()

        if completed_order_count == 0:
            raise NotFound({"error": f"No completed orders found for business_user with id {pk}"})

        # Erstelle die Daten
        data = {
            "completed_order_count": completed_order_count
        }

        # Nutze den Serializer zur Validierung und Ausgabe
        serializer = CompletedOrderCountSerializer(data)
        return Response(serializer.data)