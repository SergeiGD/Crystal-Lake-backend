"""crystallake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings

from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin_django/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('', include('apps.client_profile.additional_urls.register_urls')),
    path('', include('apps.client_profile.additional_urls.reset_password_urls')),
    path('', include('apps.client_profile.additional_urls.auth_urls')),
    path('cart/', include('apps.client_profile.additional_urls.cart_urls')),
    path('profile/', include('apps.client_profile.urls')),
    path('rooms/', include('apps.room.urls')),
    path('services/', include('apps.service.urls')),
    path('services/', include('apps.service.urls')),
    path('admin/', include('apps.worker_profile.urls')),
    path('admin/rooms/', include('apps.room.admin_urls')),
    path('admin/services/', include('apps.service.admin_urls')),
    path('admin/offers/', include('apps.offer.admin_urls')),
    path('admin/tags/', include('apps.tag.urls')),
    path('admin/groups/', include('apps.group.urls')),
    path('admin/clients/', include('apps.client.urls')),
    path('admin/workers/', include('apps.worker.urls')),
    path('admin/orders/', include('apps.order.admin_urls')),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
