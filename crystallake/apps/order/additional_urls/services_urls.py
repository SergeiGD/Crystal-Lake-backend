from django.urls import path

from ...service.views import find_services

urlpatterns = [
    path('get_services/', find_services, name='get_services_for_order'),
]
