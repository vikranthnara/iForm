from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authorization import views as app_views  # Replace with your actual app name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', app_views.register, name='register'),
    path('logout/', app_views.user_logout, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
