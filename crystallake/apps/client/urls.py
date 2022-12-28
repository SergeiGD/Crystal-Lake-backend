from django.urls import path

from .views import AdminClientsList, AdminCreateRoomView

urlpatterns = [
    path('', AdminClientsList.as_view(), name='admin_clients'),
    path('create/', AdminCreateRoomView.as_view(), name='admin_create_client'),
]
