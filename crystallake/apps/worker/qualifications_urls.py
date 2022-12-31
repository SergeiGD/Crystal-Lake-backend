from django.urls import path

from .views import get_unattached_services, add_service_to_worker, del_service_from_worker

urlpatterns = [
    path('get_unattached_services/', get_unattached_services, name='get_unattached_services'),
    path('add_service/', add_service_to_worker, name='add_service_to_worker'),
    path('del_service/', del_service_from_worker, name='del_service_from_worker'),
]