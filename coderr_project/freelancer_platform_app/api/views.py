from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .pagination import OffersPagination
from ..models import Offer, OfferDetail, Order, Profile, Review
from .serializers import BaseInfoSerializer, BusinessProfileSerializer, CompletedOrderCountSerializer, CustomerProfileSerializer, OfferSerializer, OfferDetailSerializer, FileUploadSerializer, OrderCountSerializer, OrderSerializer, ProfileSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import FileUpload
from rest_framework.views import APIView
from rest_framework import status
from .filters import OfferFilter, ReviewFilter, Updated_atOrderingFilter
from .permissions import IsCustomer, IsOwnerOrAdmin
from rest_framework.filters import OrderingFilter
from django.db import models





class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, Updated_atOrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    pagination_class = OffersPagination

    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
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
    permission_classes = [IsAdminUser]
   
    def get(self, request, format=None):
        files = FileUpload.objects.all()
        serializer = FileUploadSerializer(files, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        return Order.objects.filter(
            models.Q(customer_user=user) | models.Q(business_user=user)
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        offer_detail_id = request.data.get("offer_detail_id")
        if not offer_detail_id:
            return Response({"error": "Die ID des OfferDetails ist erforderlich."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            offer_detail = OfferDetail.objects.select_related('offer').get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response({"error": "Das angegebene OfferDetail existiert nicht."}, status=status.HTTP_404_NOT_FOUND)

        order_data = {
            "customer_user": request.user.id, 
            "business_user": offer_detail.offer.user.id, 
            "title": offer_detail.title,
            "revisions": offer_detail.revisions,
            "delivery_time_in_days": offer_detail.delivery_time_in_days,
            "price": offer_detail.price,
            "features": offer_detail.features,
            "offer_type": offer_detail.offer_type,
            "status": "in_progress",
        }

        serializer = self.get_serializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderCountView(APIView):
    def get(self, request, pk):
        order_count = Order.objects.filter(business_user=pk).count()
        
        if order_count == 0:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        data = {"order_count": order_count}
        serializer = OrderCountSerializer(data)
        return Response(serializer.data)



class CompletedOrderCountView(APIView):
    def get(self, request, pk):
        completed_order_count = Order.objects.filter(business_user=pk, status='completed').count()

        data = {
            "completed_order_count": completed_order_count
        }

        serializer = CompletedOrderCountSerializer(data)
        return Response(serializer.data)


class BaseInfoView(APIView):
    def get(self, request):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0.0
        business_profile_count = Profile.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": round(average_rating, 1),
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }

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
        profile = self.get_object()

        file_obj = request.FILES.get('file')
        if file_obj:
            file_upload = FileUpload.objects.create(image=file_obj)
            profile.file = file_upload
            profile.save()  

        return super().partial_update(request, *args, **kwargs)

class BusinessProfileViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(type='business')
    

class CustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(type='customer')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at'] 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  
        elif self.action == 'create':
            return [IsCustomer()]  
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [AllowAny()]  

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
