from django.urls import path

from ..worker.views import find_workers

urlpatterns = [
    path('get_workers/', find_workers, name='get_service_workers'),
]
