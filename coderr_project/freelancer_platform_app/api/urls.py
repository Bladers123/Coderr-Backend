from rest_framework import routers
from django.urls import path, include
from .views import OfferViewSet, OfferDetailViewSet, OrderViewSet
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

]


urlpatterns = router.urls