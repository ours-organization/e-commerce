from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('apps.products.urls', namespace='products')),
    path('register/', include('apps.register.urls', namespace='register')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
