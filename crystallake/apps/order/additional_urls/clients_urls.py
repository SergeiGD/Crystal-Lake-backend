from django.urls import path

from ...client.views import find_clients

urlpatterns = [
    path('get_clients/', find_clients, name='get_clients_for_order'),
]
