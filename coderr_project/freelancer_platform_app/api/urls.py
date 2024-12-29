from rest_framework import routers
from django.urls import path, include
from .views import OfferViewSet, OfferDetailViewSet




router = routers.DefaultRouter()


router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'offerdetails', OfferDetailViewSet, basename='offerdetail')




urlpatterns = [
    path('', include(router.urls)),
]




urlpatterns = router.urls