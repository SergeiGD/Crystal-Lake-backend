from django.urls import path

from .views import ServicesCatalog, ServiceDetail

urlpatterns = [
    path('', ServicesCatalog.as_view(), name='services'),
    path('service/<slug:service_slug>/', ServiceDetail.as_view(), name='service'),
]