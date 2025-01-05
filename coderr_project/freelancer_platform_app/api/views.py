from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .permissons import IsOwnerOrReadOnly
from ..models import BusinessProfile, CustomerProfile, Offer, OfferDetail, Order, Profile, Review
from .serializers import BaseInfoSerializer, BusinessProfileSerializer, CompletedOrderCountSerializer, CustomerProfileSerializer, OfferSerializer, OfferDetailSerializer, FileUploadSerializer, OrderCountSerializer, OrderSerializer, ProfileSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import FileUpload
from rest_framework.views import APIView
from rest_framework import status
from .filters import OfferFilter
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from django.core.exceptions import PermissionDenied




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
    



class BaseInfoView(APIView):
    def get(self, request):
        
        # Anzahl der Offers
        offer_count = Offer.objects.count()

        # Erstelle die Daten
        data = {
            "offer_count": offer_count,
            "review_count": 10,
            "average_rating": 4.6,
            "business_profile_count": 45,
        }

        # Nutze den Serializer zur Validierung und Ausgabe
        serializer = BaseInfoSerializer(data)
        return Response(serializer.data)
    

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_permissions(self):
        """
        Bestimmt die benötigten Berechtigungen je nach ViewSet-Aktion.
        """
        if self.action == 'list':
            # Nur Admin-User dürfen die Liste aller Profile sehen
            permission_classes = [IsAdminUser]
        else:
            # Bei allen anderen Aktionen (retrieve, update, delete etc.) 
            # muss der User zumindest eingeloggt sein.
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Gibt das passende QuerySet je nach User und Aktion zurück:
        - Admin sieht immer alle Profile.
        - Normale User (nicht Admin) sehen bei Detail-Ansichten nur ihr eigenes Profil.
        - In der Listenansicht (action == 'list') gibt es für normale User dank get_permissions() kein Zugriff.
        """
        if self.request.user.is_staff:
            # Admin darf immer alle Profile sehen
            return Profile.objects.all()
        else:
            # Normaler User sieht (bei Detail-Ansichten) nur das eigene Profil
            return Profile.objects.filter(user=self.request.user)






class BusinessProfileViewSet(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer



class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer




class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
