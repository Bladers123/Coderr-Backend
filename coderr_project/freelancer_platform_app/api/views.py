from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from ..models import Offer, OfferDetail, Order, Profile, Review
from .serializers import BaseInfoSerializer, BusinessProfileSerializer, CompletedOrderCountSerializer, CustomerProfileSerializer, OfferSerializer, OfferDetailSerializer, FileUploadSerializer, OrderCountSerializer, OrderSerializer, ProfileSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import FileUpload
from rest_framework.views import APIView
from rest_framework import status
from .filters import OfferFilter
from django.contrib.auth import get_user_model
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                "count": self.paginator.page.paginator.count,
                "results": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": len(queryset),
            "results": serializer.data
        })

    def perform_create(self, serializer):
        # Hier überschreiben wir den user-Feldwert und setzen ihn 
        # auf den aktuell eingeloggten Benutzer (request.user).
        serializer.save(user=self.request.user)


class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.select_related('offer').all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                "count": self.paginator.page.paginator.count,
                "results": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": len(queryset),
            "results": serializer.data
        })





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
        return Response({}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        # Prüfe, ob `offer_detail_id` in der Anfrage vorhanden ist
        offer_detail_id = request.data.get("offer_detail_id")
        if not offer_detail_id:
            return Response(
                {"error": "Die ID des OfferDetails ist erforderlich."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Suche nach dem OfferDetail
        try:
            offer_detail = OfferDetail.objects.select_related('offer').get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response(
                {"error": "Das angegebene OfferDetail existiert nicht."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Bereite die Daten aus dem OfferDetail vor
        order_data = {
            "customer_user": request.user.id,  # Kunde ist der aktuelle Benutzer
            "business_user": offer_detail.offer.user.id,  # Anbieter aus Offer
            "title": offer_detail.title,
            "revisions": offer_detail.revisions,
            "delivery_time_in_days": offer_detail.delivery_time_in_days,
            "price": offer_detail.price,
            "features": offer_detail.features,
            "offer_type": offer_detail.offer_type,
            "status": "in_progress",  # Standardstatus
        }

        # Serialisiere die Daten und erstelle die Bestellung
        serializer = self.get_serializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






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
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

   
    def partial_update(self, request, *args, **kwargs):
        # Das aktuelle Profile-Objekt abrufen
        profile = self.get_object()

        # Datei-Upload prüfen und speichern
        file_obj = request.FILES.get('file')
        if file_obj:
            # Neues FileUpload-Objekt erstellen
            file_upload = FileUpload.objects.create(image=file_obj)
            # Profile-Objekt mit dem neuen FileUpload verknüpfen
            profile.file = file_upload
            profile.save()  # Speichern, um die Änderung in die DB zu übernehmen

        # Standard-Update-Logik von DRF aufrufen (für andere Felder)
        return super().partial_update(request, *args, **kwargs)

class BusinessProfileViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessProfileSerializer

    def get_queryset(self):
        # Filtert nur Profile mit type='business'
        return Profile.objects.filter(type='business')
    

class CustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer

    def get_queryset(self):
        # Filtert nur Profile mit type='customer'
        return Profile.objects.filter(type='customer')



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
