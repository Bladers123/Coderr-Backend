from django.urls import path
from rest_framework import routers
from .views import UsersViewSet, RegistrationsViewSet, LoginView

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet, basename='user-auth')
router.register(r'registration', RegistrationsViewSet, basename='user-registration')

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
]

urlpatterns += router.urls
