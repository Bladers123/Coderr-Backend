from rest_framework import routers
from django.urls import path, include
from .views import OfferViewSet, OfferDetailViewSet, OrderViewSet, OrderCountView, CompletedOrderCountView, BaseInfoView, ProfileViewSet, BusinessProfileViewSet, CustomerProfileViewSet, ReviewViewSet
from django.conf import settings
from django.conf.urls.static import static
from .views import FileUploadView




router = routers.DefaultRouter()


router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'offerdetails', OfferDetailViewSet, basename='offerdetail')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'profiles/business', BusinessProfileViewSet, basename='businessprofile')
router.register(r'profiles/customer', CustomerProfileViewSet, basename='customerprofile')
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('', include(router.urls)),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
    path('base-info/', BaseInfoView.as_view(), name='base-info')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)