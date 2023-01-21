from django.urls import path

from ..views import room_purchase_create_view, room_purchase_edit_view, service_purchase_create_view, service_purchase_edit_view, get_purchase_info_view, cancel_purchase_view

urlpatterns = [
    # TODO: СДЕЛАТЬ КАК С ТАМЙМТЕЙБЛ
    path('edit_room_purchase/<int:purchase_id>/', room_purchase_edit_view, name='edit_room_purchase'),
    path('create_room_purchase/', room_purchase_create_view, name='create_room_purchase'),
    path('edit_service_purchase/<int:purchase_id>/', service_purchase_edit_view, name='edit_service_purchase'),
    path('create_service_purchase/', service_purchase_create_view, name='create_service_purchase'),
    # path('manage_service_purchase/', service_purchase_manage_view, name='manage_service_purchase'),
    path('get_purchase/<int:purchase_id>/', get_purchase_info_view, name='get_purchase'),
    path('cancel_purchase/<int:purchase_id>/', cancel_purchase_view, name='cancel_purchase'),
]
