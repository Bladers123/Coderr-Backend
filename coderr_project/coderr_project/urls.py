from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('authentication_app.api.urls')),
    path('api/', include('freelancer_platform_app.api.urls'))
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)