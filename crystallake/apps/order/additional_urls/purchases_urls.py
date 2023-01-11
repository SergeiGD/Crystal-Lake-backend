from django.urls import path

from ..views import room_purchase_manage_view, service_purchase_manage_view, get_purchase_info_view, cancel_purchase_view

urlpatterns = [
    path('manage_room_purchase/', room_purchase_manage_view, name='manage_room_purchase'),
    path('manage_service_purchase/', service_purchase_manage_view, name='manage_service_purchase'),
    path('get_purchase/<int:purchase_id>/', get_purchase_info_view, name='get_purchase'),
    path('cancel_purchase/<int:purchase_id>/', cancel_purchase_view, name='cancel_purchase'),
]
