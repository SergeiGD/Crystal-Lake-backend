from django.urls import path

from .views import AdminClientsList, AdminCreatClient, AdminClientDetail, AdminClientUpdate, admin_delete_client

urlpatterns = [
    path('', AdminClientsList.as_view(), name='admin_clients'),
    path('create/', AdminCreatClient.as_view(), name='admin_create_client'),
    path('show/<int:client_id>/', AdminClientDetail.as_view(), name='admin_show_client'),
    path('edit/<int:client_id>/', AdminClientUpdate.as_view(), name='admin_edit_client'),
    path('delete/<int:client_id>/', admin_delete_client, name='admin_delete_client'),
]
