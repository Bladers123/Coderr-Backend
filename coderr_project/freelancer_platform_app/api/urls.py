from rest_framework import routers
from django.urls import path, include
from .views import OfferViewSet, OfferDetailViewSet, OrderViewSet, OrderCountView, CompletedOrderCountView
from django.conf import settings
from django.conf.urls.static import static
from .views import FileUploadView




router = routers.DefaultRouter()


router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'offerdetails', OfferDetailViewSet, basename='offerdetail')
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)